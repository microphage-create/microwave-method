"""gate_embodiment: the agent has a body when it needs one.

A body (name, icon, palette, then `embodied: true` with the icon file) is
mandatory for an agent that can do damage (write/spend/prod), so it is
recognizable among live sessions. A read-only agent may activate bodiless:
its embodiment block is optional (ADR-003 amended, not the old ADR-004).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter, repo_root

GATE = "gate_embodiment"
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def main(card: str) -> None:
    path = Path(card)
    try:
        fm, _ = read_frontmatter(path)
    except GateError as e:
        fail(GATE, str(e))
    root = repo_root(path.parent)
    powerful = get(fm, "blast_radius") in ("write", "spend", "prod")

    name = str(get(fm, "embodiment.display_name") or "").strip()
    icon = str(get(fm, "embodiment.icon") or "").strip()

    # A read-only agent with no embodiment block is legitimately bodiless.
    if not powerful and not name and not icon:
        ok(GATE, f"{path.name}: read-only, bodiless (embodiment optional)")
        return

    if not name:
        fail(GATE, f"{path.name}: embodiment.display_name is empty")
    if not icon:
        fail(GATE, f"{path.name}: embodiment.icon is empty")
    for key in ("bg", "fg", "accent"):
        val = str(get(fm, f"embodiment.palette.{key}") or "")
        if not HEX.match(val):
            fail(GATE, f"{path.name}: embodiment.palette.{key}={val!r} is not #rrggbb")

    if get(fm, "embodiment.embodied") is True and not (root / icon).exists():
        fail(GATE, f"{path.name}: embodied is true but icon file not found: {icon}")
    # Embodiment is mandatory only for agents that can do damage (ADR-003):
    # a read-only agent may activate bodiless. write/spend/prod must have a
    # body, so it is recognizable among live sessions.
    powerful = get(fm, "blast_radius") in ("write", "spend", "prod")
    if get(fm, "status") == "active" and powerful:
        if get(fm, "embodiment.embodied") is not True:
            fail(GATE, f"{path.name}: a {get(fm, 'blast_radius')} agent must be "
                       f"embodied before activation. Run: "
                       f"python embodiment/embody.py {card}")
        if not (root / icon).exists():
            fail(GATE, f"{path.name}: icon file not found: {icon}")
    embodied = get(fm, "embodiment.embodied") is True
    ok(GATE, f"{path.name}: body manifest ok"
             + (" and embodied" if embodied
                else " (read-only, body optional)" if not powerful
                else " (staging)"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/gate_embodiment.py <agent-card.md>")
    main(sys.argv[1])
