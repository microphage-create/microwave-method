"""run_gates: the full pipeline on one agent card.

anti-dup → brief → schema → testable → embodiment → slop → wiki.
Exit code 0 = all green = the card may activate (fast path) or go to the
gatekeeper (full path). Any red gate stops the pipeline with its message.
"""
import subprocess
import sys
from pathlib import Path

GATES = [
    "gate_antidup.py",
    "gate_brief.py",
    "gate_schema.py",
    "gate_testable.py",
    "gate_embodiment.py",
    "gate_slop.py",
    "gate_wiki.py",
]


def main(card: str) -> None:
    here = Path(__file__).parent
    for gate in GATES:
        res = subprocess.run([sys.executable, str(here / gate), card])
        if res.returncode != 0:
            print(f"\n[run_gates] STOPPED at {gate}. Fix and re-run.")
            sys.exit(res.returncode)
    print(f"\n[run_gates] ALL GREEN for {card}. "
          f"Fast path: activate. Full path: request gatekeeper judgment.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python gates/run_gates.py <agent-card.md>")
        sys.exit(1)
    main(sys.argv[1])
