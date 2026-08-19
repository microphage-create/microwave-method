"""gate_docs: generated doc sections match their source.

The README carries sections DERIVED from the repo (the gate list, and more
later), filled by gates/docgen.py and frozen between markers. This gate is the
freshness check of that materialized view (ADR-022): it fails when the frozen
text no longer equals what the formula produces, so a doc cannot silently rot.
Fix: run `python gates/docgen.py` and commit.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, ok, repo_root
import docgen

GATE = "gate_docs"


def main() -> None:
    stale = docgen.apply(repo_root(), check=True)
    if stale:
        fail(GATE, f"generated doc sections are stale: {', '.join(stale)}. "
                   f"Run `python gates/docgen.py` and commit the result.")
    ok(GATE, "generated doc sections match their source")


if __name__ == "__main__":
    try:
        main()
    except GateError as e:
        fail(GATE, str(e))
