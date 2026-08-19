"""gate_testable: every done-criterion names a check (form, not execution).

Gates verify existence and substance of checks, not their pertinence: that is
the gatekeeper's job on the full path, and post-hoc trace review everywhere.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter

GATE = "gate_testable"

HOLLOW = {"true", "yes", "ok", "works", "done", "n/a", "todo", "tbd", "manual",
          "see above", "obvious"}


def is_hollow(check: str) -> bool:
    """Hollow = a bare filler word, or a single token that names no command.
    'pytest -q' (has an argument) and 'python gates/gate_wiki.py' pass;
    'works' and 'done' do not."""
    low = check.lower().strip()
    if low in HOLLOW:
        return True
    words = low.split()
    return len(words) == 1 and not any(ch in low for ch in "./-_")


def main(card: str) -> None:
    path = Path(card)
    try:
        fm, _ = read_frontmatter(path)
    except GateError as e:
        fail(GATE, str(e))
    crits = get(fm, "brief.success_criteria") or []
    if not crits:
        fail(GATE, f"{path.name}: no success criteria to check")
    for i, c in enumerate(crits, 1):
        check = str(c.get("check", "")).strip() if isinstance(c, dict) else ""
        if not check:
            fail(GATE, f"{path.name}: criterion #{i} has no check "
                       f"('{c.get('criterion', '?') if isinstance(c, dict) else c}')")
        if is_hollow(check):
            fail(GATE, f"{path.name}: criterion #{i} check is hollow: {check!r}. "
                       f"Name a command or a measurable assertion.")
    ok(GATE, f"{path.name}: {len(crits)} criteria, all tied to substantive checks")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/gate_testable.py <agent-card.md>")
    main(sys.argv[1])
