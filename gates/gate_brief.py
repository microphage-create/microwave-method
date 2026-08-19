"""gate_brief: the 3-section brief is complete.

Success criteria, volume cap, abort conditions. A brief missing one section
does not launch (the rule behind it: autonomous work without these three
produces chaos).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter

GATE = "gate_brief"


def main(card: str) -> None:
    path = Path(card)
    try:
        fm, _ = read_frontmatter(path)
    except GateError as e:
        fail(GATE, str(e))

    crits = get(fm, "brief.success_criteria")
    if not isinstance(crits, list) or not crits:
        fail(GATE, f"{path.name}: brief.success_criteria is empty")
    for i, c in enumerate(crits, 1):
        if not isinstance(c, dict) or not c.get("criterion"):
            fail(GATE, f"{path.name}: success_criteria #{i} has no 'criterion'")

    cap = get(fm, "brief.volume_cap")
    if not cap or not any(ch.isdigit() for ch in str(cap)):
        fail(GATE, f"{path.name}: brief.volume_cap must state a number (got {cap!r})")

    aborts = get(fm, "brief.abort_conditions")
    if not isinstance(aborts, list) or not aborts or not all(str(a).strip() for a in aborts):
        fail(GATE, f"{path.name}: brief.abort_conditions is empty")

    ok(GATE, f"{path.name}: 3-section brief complete "
             f"({len(crits)} criteria, cap set, {len(aborts)} abort conditions)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/gate_brief.py <agent-card.md>")
    main(sys.argv[1])
