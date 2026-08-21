"""run_gates: the full pipeline on one agent card.

anti-dup → brief → schema → testable → embodiment → uses → slop → wiki.
Exit code 0 = all green = the card may activate (fast path) or go to the
gatekeeper (full path). ALL gates run every time, even after one goes red, so
the fix list is complete in one pass rather than surfacing one red at a time.
"""
import os
import subprocess
import sys
from pathlib import Path

# run_gates now decodes and re-prints each gate's output, so it must be as
# console-safe as the gates themselves (_lib hardens their stdout the same way):
# on a non-UTF-8 console (Windows cp1252) re-printing a gate's fancy character
# must not crash run_gates with UnicodeEncodeError.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass

GATES = [
    "gate_antidup.py",
    "gate_brief.py",
    "gate_schema.py",
    "gate_testable.py",
    "gate_embodiment.py",
    "gate_uses.py",
    "gate_slop.py",
    "gate_wiki.py",
]


def main(card: str) -> None:
    here = Path(__file__).parent
    failed: list[tuple[str, str]] = []
    for gate in GATES:
        res = subprocess.run([sys.executable, str(here / gate), card],
                             capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        out = (res.stdout + res.stderr).strip()
        if out:
            print(out)  # keep each gate's own line in the running log
        if res.returncode != 0:
            last = out.splitlines()[-1] if out else "(no output)"
            failed.append((gate, last))

    if failed:
        print(f"\n[run_gates] {len(failed)} of {len(GATES)} gates RED for {card} "
              f"(all gates ran; fix these together, then re-run):")
        for gate, msg in failed:
            print(f"  FAIL  {gate}: {msg}")
        sys.exit(1)
    if os.environ.get("MICROWAVE_SHADOW") == "1":
        print(f"\n[run_gates] SHADOW MODE: gates ran report-only. Any 'would block' "
              f"line above is NOT enforced; unset MICROWAVE_SHADOW to enforce. "
              f"This is not a green result.")
    else:
        print(f"\n[run_gates] ALL GREEN for {card}. "
              f"Fast path: activate. Full path: request gatekeeper judgment.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python gates/run_gates.py <agent-card.md>")
        sys.exit(1)
    main(sys.argv[1])
