"""gate_uses: an agent's declared services actually exist in the registry.

A context agent wires transversal services (`uses: [copywriter, code-review]`).
Each slug must resolve to a SERVICE card in the registry, so a typo or a service
that was never created is caught here, not silently at runtime. Services can live
in a shared repo federated in via .microwave/federation, so resolution spans the
federation (a context in repo A may use a service defined in repo B). No `uses`
means nothing to check.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter, repo_root
from federated_index import federated_index_lines

GATE = "gate_uses"
# an index line for a service: "- [service] <slug>: ..."
SERVICE_RE = re.compile(r"^-\s*\[service\]\s+([a-z0-9][a-z0-9-]*)\b")


def _service_slugs(root: Path) -> set[str]:
    slugs = set()
    for _src, line in federated_index_lines(root):
        m = SERVICE_RE.match(line.strip())
        if m:
            slugs.add(m.group(1))
    return slugs


def main(card: str) -> None:
    path = Path(card)
    try:
        fm, _ = read_frontmatter(path)
    except GateError as e:
        fail(GATE, str(e))
    uses = get(fm, "uses") or []
    if isinstance(uses, str):
        uses = [uses]
    wanted = [str(u).strip() for u in uses if str(u).strip()]
    if not wanted:
        ok(GATE, f"{path.name}: declares no services")
        return
    services = _service_slugs(repo_root(path.parent))
    missing = [u for u in wanted if u not in services]
    if missing:
        fail(GATE, f"{path.name}: uses names service(s) not in the registry: "
                   f"{', '.join(missing)}. Create the service card, fix the slug, "
                   f"or federate the repo that holds it (.microwave/federation).")
    ok(GATE, f"{path.name}: {len(wanted)} service(s) resolve")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/gate_uses.py <agent-card.md>")
    try:
        main(sys.argv[1])
    except GateError as e:
        fail(GATE, str(e))
