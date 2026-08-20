"""gate_testable: every done-criterion names a real check, not a filler word.

It checks the FORM of a check (it names a command or assertion) and that any
`gates/<name>.py` it invokes actually exists, so a criterion cannot point at a
gate that does not exist. It does NOT run the check or judge its pertinence:
that is the gatekeeper's job on the full path, and post-hoc trace review.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter, repo_root_or_cwd

GATE = "gate_testable"
GATE_REF_RE = re.compile(r"\bgates/(\w+\.py)\b")

HOLLOW = {"true", "yes", "ok", "works", "done", "n/a", "todo", "tbd", "manual",
          "see above", "obvious"}


def is_hollow(check: str) -> bool:
    """Hollow = a bare filler word, or a single token that names no command.
    'pytest -q' (has an argument) and 'python gates/gate_wiki.py' pass;
    'works' and 'done' do not."""
    low = check.lower().strip()
    if low.rstrip(".!,;:") in HOLLOW:  # 'done.' is as hollow as 'done'
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
    root = repo_root_or_cwd(path.resolve().parent)
    # None only for a truly isolated card (unit test in a bare tmp dir); the hook
    # validates a staged blob in a tmp path, so the Path.cwd() fallback finds the
    # real repo and the ref-check still runs at commit time.
    for i, c in enumerate(crits, 1):
        check = str(c.get("check", "")).strip() if isinstance(c, dict) else ""
        if not check:
            fail(GATE, f"{path.name}: criterion #{i} has no check "
                       f"('{c.get('criterion', '?') if isinstance(c, dict) else c}')")
        if is_hollow(check):
            fail(GATE, f"{path.name}: criterion #{i} check is hollow: {check!r}. "
                       f"Name a command or a measurable assertion.")
        if root is not None:
            for ref in GATE_REF_RE.findall(check):
                if not (root / "gates" / ref).exists():
                    fail(GATE, f"{path.name}: criterion #{i} names gates/{ref}, "
                               f"which does not exist. Name a real gate or fix the path.")
    ok(GATE, f"{path.name}: {len(crits)} criteria, all tied to substantive checks")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/gate_testable.py <agent-card.md>")
    main(sys.argv[1])
