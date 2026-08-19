"""activate: tooled, re-validated activation of a staged agent card.

Fast path (blast_radius: read): run by the creator once gates are green.
Full path: run by the gatekeeper as the act of judgment.

Does, in order:
1. run the full gate pipeline on the staged card (pre-check)
2. move the card from wiki/_staging/ to wiki/agents/, set `status: active`
3. append the registry line to wiki/INDEX.md
4. re-run the full gate pipeline on the ACTIVATED card (post-check):
   the state that ships is the state that was validated
On any post-check failure the activation is rolled back.
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter, repo_root

GATE = "activate"


def run_pipeline(card: Path) -> bool:
    res = subprocess.run([sys.executable, str(Path(__file__).parent / "run_gates.py"), str(card)])
    return res.returncode == 0


def main(card_arg: str) -> None:
    src = Path(card_arg).resolve()
    root = repo_root(src.parent)
    if "_staging" not in src.parts:
        fail(GATE, f"{src.name}: activation starts from wiki/_staging/ (got {src})")
    try:
        fm, _ = read_frontmatter(src)
    except GateError as e:
        fail(GATE, str(e))
    slug = str(get(fm, "slug"))
    mission = str(get(fm, "mission") or "").rstrip(".")

    if not run_pipeline(src):
        fail(GATE, "pre-check failed: fix the gates before activating")

    dst = root / "wiki" / "agents" / f"{slug}.md"
    if dst.exists():
        fail(GATE, f"{dst} already exists")

    text = src.read_text(encoding="utf-8")
    new_text, n = re.subn(r"^status: staging$", "status: active", text,
                          count=1, flags=re.M)
    if n != 1:
        fail(GATE, f"{src.name}: could not flip 'status: staging' to active")
    dst.write_text(new_text, encoding="utf-8")

    index = root / "wiki" / "INDEX.md"
    idx_text = index.read_text(encoding="utf-8-sig")
    line = f"- [agent] {slug}: {mission} → wiki/agents/{slug}.md"
    inserted = False
    if line not in idx_text:
        if "## Agents\n" not in idx_text:
            dst.unlink()
            fail(GATE, "wiki/INDEX.md has no '## Agents' section: restore the "
                       "heading before activating")
        idx_text = idx_text.replace("## Agents\n", f"## Agents\n\n{line}\n", 1)
        index.write_text(idx_text, encoding="utf-8")
        inserted = True

    src.unlink()

    if not run_pipeline(dst):
        # rollback: restore staging state, symmetric with the insertion
        dst_text = dst.read_text(encoding="utf-8")
        src.write_text(dst_text.replace("status: active", "status: staging", 1),
                       encoding="utf-8")
        dst.unlink()
        if inserted:
            index.write_text(idx_text.replace(f"\n{line}\n", "", 1), encoding="utf-8")
        fail(GATE, "post-check failed on the activated card: rolled back to staging")

    ok(GATE, f"{slug} activated, registered, and re-validated in its final state")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/activate.py wiki/_staging/<slug>.md")
    main(sys.argv[1])
