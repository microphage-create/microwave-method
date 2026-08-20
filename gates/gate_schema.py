"""gate_schema: the agent card matches the template contract.

Also cross-checks the declared blast radius against write-signals in the
card's outputs and Interfaces section: a `read` agent whose card says it
writes is rejected (the ceremony selector must not rest on goodwill). The
check is a heuristic; its rule of thumb is documented in the flow: when in
doubt, full path.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter

GATE = "gate_schema"

REQUIRED = [
    "type", "kind", "name", "slug", "status", "blast_radius", "mission",
    "definition_path", "owner", "synonyms",
    "brief.success_criteria", "brief.volume_cap", "brief.abort_conditions",
]
# The embodiment manifest is required only for agents that can do damage
# (ADR-003/004 amended): a read-only agent may carry no embodiment block.
EMBODIMENT_REQUIRED = [
    "embodiment.display_name", "embodiment.icon", "embodiment.palette.bg",
    "embodiment.palette.fg", "embodiment.palette.accent",
]
ENUMS = {
    "type": {"agent-card"},
    "kind": {"context", "service"},
    "status": {"staging", "active", "rejected"},
    "blast_radius": {"read", "write", "spend", "prod"},
}
# identity strings end up in terminal profiles and launchers: keep them tame
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.-]{0,31}$")
# embodiment.launch is interpolated into a shell command by the OS adapters:
# forbid every shell metacharacter so a crafted card cannot run code.
LAUNCH_FORBIDDEN = re.compile(r"""[;&|`$<>(){}\[\]"'\\\n\r]""")
# write-signals for the read-vs-declared cross-check: fleshed verb forms only,
# so nouns like "deploy log" or "commit history" do not trip a read agent.
WRITE_SIGNALS = re.compile(
    r"\b(writes|creates|deletes|deploys|deployed|updates|edits|edited|"
    r"modifies|modified|pushes|pushed|commits|committed|sends|spends|"
    r"purchases|registers)\b", re.I)


def main(card: str) -> None:
    path = Path(card)
    try:
        fm, body = read_frontmatter(path)
    except GateError as e:
        fail(GATE, str(e))
    powerful = get(fm, "blast_radius") in ("write", "spend", "prod")
    required = REQUIRED + (EMBODIMENT_REQUIRED if powerful else [])
    missing = [k for k in required if get(fm, k) in (None, "", [])]
    if missing:
        fail(GATE, f"{path.name}: missing/empty fields: {', '.join(missing)}")
    for field, allowed in ENUMS.items():
        val = get(fm, field)
        if val not in allowed:
            fail(GATE, f"{path.name}: {field}={val!r}, expected one of {sorted(allowed)}")
    slug = str(get(fm, "slug"))
    if path.stem != slug:
        fail(GATE, f"{path.name}: filename must equal slug '{slug}'")
    if not SLUG_RE.match(slug):
        fail(GATE, f"{path.name}: slug {slug!r} must match {SLUG_RE.pattern}")
    # a context agent guards one repo, so it must name it; a service is
    # transversal and names none. (kind is enum-checked above.)
    if get(fm, "kind") == "context" and get(fm, "repo") in (None, "", []):
        fail(GATE, f"{path.name}: a context agent must name the repo it guards "
                   f"(add 'repo: <name-or-path>'); a service agent omits it.")
    if get(fm, "kind") == "service" and get(fm, "repo") not in (None, "", []):
        fail(GATE, f"{path.name}: a service agent is transversal and names no repo; "
                   f"remove 'repo:', or set kind: context.")
    if "→" in str(get(fm, "mission") or ""):
        fail(GATE, f"{path.name}: mission must not contain '→'; it delimits the "
                   f"registry line, so it would corrupt the index. Reword the mission.")
    # embodiment identity is validated only when the block is present
    # (mandatory for powerful agents, optional for read-only)
    if get(fm, "embodiment.display_name") not in (None, ""):
        name = str(get(fm, "embodiment.display_name"))
        if not NAME_RE.match(name):
            fail(GATE, f"{path.name}: display_name {name!r} must match "
                       f"{NAME_RE.pattern} (it ends up in terminal profiles)")
    launch = get(fm, "embodiment.launch")
    if launch not in (None, "") and LAUNCH_FORBIDDEN.search(str(launch)):
        fail(GATE, f"{path.name}: embodiment.launch {launch!r} contains a shell "
                   f"metacharacter. It is run by the launcher; keep it to a bare "
                   f"command and arguments, or drop it.")

    if get(fm, "blast_radius") == "read":
        outputs = " ".join(str(o) for o in (get(fm, "outputs") or []))
        interfaces = ""
        m = re.search(r"##\s*Interfaces\s*\n(.*?)(\n##|\Z)", body, re.S)
        if m:
            interfaces = m.group(1)
        blob = outputs + " " + interfaces
        # a write-verb negated ("never writes", "no writes", "writes nothing")
        # is a read declaration, not a write-signal: do not flag it
        hits = sorted({mt.group(0).lower() for mt in WRITE_SIGNALS.finditer(blob)
                       if not re.search(r"\b(never|no|not|n't)\s+$", blob[:mt.start()])
                       and not blob[mt.end():].lstrip().lower().startswith("nothing")})
        if hits:
            fail(GATE, f"{path.name}: blast_radius is 'read' but the card "
                       f"declares write-signals: {', '.join(hits)}. This is a "
                       f"heuristic tripwire, not the real guard: raise the blast "
                       f"radius (full path, where the devil pass and gatekeeper "
                       f"actually judge privilege) or fix the card.")

    ok(GATE, f"{path.name} conforms to the card contract")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/gate_schema.py <agent-card.md>")
    try:
        main(sys.argv[1])
    except GateError as e:
        fail(GATE, str(e))
