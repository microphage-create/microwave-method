"""Regression guards for flow-prose invariants (IR-002, IR-003).

Flows are prose protocols: their behavior IS their text, so the regression
test for a protocol amendment asserts the mandate's anchor phrases are
present. Keyed on short, meaning-bearing phrases (not full sentences) so
wording can be polished without breaking the guard, while dropping the
mandate itself still fails loudly.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEVIL_REVIEW = ROOT / "flows" / "devil-review.md"
DEVIL_REPORT = ROOT / "templates" / "devil-report.md"


class TestDevilReviewProtocol(unittest.TestCase):
    def setUp(self):
        # prose is hard-wrapped; collapse whitespace so anchors survive re-wraps
        self.text = " ".join(DEVIL_REVIEW.read_text(encoding="utf-8").split())

    def test_estate_fact_check_is_mandated(self):
        """IR-002: a by-the-book devil must fact-check the estate, not rely on
        the spawn prompt granting it ad hoc."""
        self.assertIn("READ-ONLY access to the reality", self.text)
        self.assertIn("Verify before you judge", self.text)
        # a contradicted safety claim must map to the KILL row, and the
        # verdict block must carry the verification counts
        self.assertIn("the estate contradicts", self.text)
        self.assertIn("Facts:", self.text)

    def test_criteria_surface_must_be_exhausted(self):
        """IR-003: all bypasses of a criterion in one round, and never-touch
        criteria get a transport enumeration."""
        self.assertIn("no further bypass found", self.text)
        self.assertIn("enumerate every transport", self.text)
        self.assertIn("weakest transport", self.text)

    def test_unverifiable_is_not_a_safe_harbor(self):
        """IR-002 hardening: an unverifiable-by-nature safety claim is an
        objection (row 2b), not a pass; access failures blame the
        orchestrator's provisioning, not the card."""
        self.assertIn("| 2b | blast radius |", self.text)
        self.assertIn("not a safe harbor", self.text)
        self.assertIn("unverifiable (access)", self.text.lower())

    def test_severities_are_deterministic(self):
        """Round-2 hardening: unnamed transports and ordinary contradictions
        have their own rows, and multi-row findings resolve by precedence."""
        self.assertIn("| 3b | criteria |", self.text)
        self.assertIn("| 7 | facts |", self.text)
        self.assertIn("most severe matching row", self.text)

    def test_loop_provisions_the_devil(self):
        loop = " ".join((ROOT / "flows" / "devil-loop.md")
                        .read_text(encoding="utf-8").split())
        self.assertIn("PROVISIONS each devil", loop)
        self.assertIn("unverifiable (access)", loop)

    def test_report_template_carries_the_facts_slot(self):
        """The verification counts must reach the record the gatekeeper
        reads, not die at the end of each round."""
        report = " ".join(DEVIL_REPORT.read_text(encoding="utf-8").split())
        self.assertIn("Facts:", report)
        self.assertIn("one line per claim", report)


if __name__ == "__main__":
    unittest.main()
