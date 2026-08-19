"""Integration tests for the gates: run each gate as a subprocess on real
fixtures and assert the exit code and message. Stdlib only (ADR-007).

Run: python -m unittest discover tests
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATES = Path(__file__).resolve().parent.parent / "gates"

VALID_READ_CARD = """---
type: agent-card
name: Test Reader
slug: test-reader
status: staging
blast_radius: read
mission: read files and report what they contain
definition_path: flows/test-reader.md
owner: "@me"
synonyms: [reader, scanner]
brief:
  success_criteria:
    - "the report lists every file (check: a test counts files and compares)"
  volume_cap: 10 files per run
  abort_conditions: stop if a path escapes the target folder
---

# Test Reader

## Interfaces

Reads the target folder. Writes nothing.
"""


def run_gate(gate: str, card: Path):
    r = subprocess.run([sys.executable, str(GATES / gate), str(card)],
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def write_card(text: str, slug: str = "test-reader") -> Path:
    d = Path(tempfile.mkdtemp())
    p = d / f"{slug}.md"
    p.write_text(text, encoding="utf-8")
    return p


class TestGateSchema(unittest.TestCase):
    def test_valid_read_card_passes(self):
        rc, out = run_gate("gate_schema.py", write_card(VALID_READ_CARD))
        self.assertEqual(rc, 0, out)

    def test_missing_required_field_fails(self):
        bad = VALID_READ_CARD.replace('owner: "@me"\n', "")
        rc, out = run_gate("gate_schema.py", write_card(bad))
        self.assertEqual(rc, 1)
        self.assertIn("owner", out)

    def test_bad_enum_fails(self):
        bad = VALID_READ_CARD.replace("blast_radius: read", "blast_radius: godmode")
        rc, out = run_gate("gate_schema.py", write_card(bad))
        self.assertEqual(rc, 1)

    def test_filename_must_equal_slug(self):
        rc, out = run_gate("gate_schema.py",
                           write_card(VALID_READ_CARD, slug="wrong-name"))
        self.assertEqual(rc, 1)

    def test_read_card_with_write_signal_fails(self):
        bad = VALID_READ_CARD.replace("Writes nothing.",
                                      "It writes a summary file and commits it.")
        rc, out = run_gate("gate_schema.py", write_card(bad))
        self.assertEqual(rc, 1)

    def test_read_card_negated_write_verb_passes(self):
        # "never writes" / "writes nothing" must NOT trip the write-signal guard
        ok = VALID_READ_CARD.replace("Writes nothing.",
                                     "It never writes and it writes nothing.")
        rc, out = run_gate("gate_schema.py", write_card(ok))
        self.assertEqual(rc, 0, out)


if __name__ == "__main__":
    unittest.main()
