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
kind: service
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


def repo_with_index(index_body: str) -> Path:
    root = Path(tempfile.mkdtemp())
    (root / "wiki").mkdir()
    (root / "wiki" / "INDEX.md").write_text(index_body, encoding="utf-8")
    return root


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


GHOST_GATE_CARD = """---
type: agent-card
kind: service
name: Ghost Ref
slug: ghost-ref
status: staging
blast_radius: read
mission: read files and report what they contain
definition_path: flows/ghost-ref.md
owner: "@me"
synonyms: [reader, scanner]
brief:
  success_criteria:
    - criterion: it reports every file
      check: python gates/ghost.py passes
  volume_cap: 5 files per run
  abort_conditions: stop if a path escapes the folder
---

# Ghost Ref

Reads the folder. Writes nothing.
"""


class TestDecay(unittest.TestCase):
    def test_flags_orphan_old_atom_keeps_linked(self):
        import tempfile
        root = Path(tempfile.mkdtemp())
        d = root / "wiki" / "projects" / "x" / "learnings"
        d.mkdir(parents=True)
        (root / "wiki" / "INDEX.md").write_text("# idx\n", encoding="utf-8")
        (d / "LRN-A.md").write_text("# A\nalive\n", encoding="utf-8")
        (d / "LRN-B.md").write_text("# B\nsee [[LRN-A]]\n", encoding="utf-8")
        (d / "LRN-C.md").write_text("# C\norphan\n", encoding="utf-8")
        git = ["git", "-C", str(root)]
        subprocess.run(git + ["init", "-q"], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["-c", "user.email=t@t", "-c", "user.name=t",
                              "commit", "-qm", "seed"], check=True)
        sys.path.insert(0, str(GATES))
        import decay
        names = {Path(s["atom"]).name for s in decay.find_stale(root, 0.0)}
        self.assertIn("LRN-C.md", names)      # orphan -> candidate
        self.assertNotIn("LRN-A.md", names)   # linked -> alive


class TestShadowMode(unittest.TestCase):
    def test_shadow_reports_but_does_not_block(self):
        import os
        bad = VALID_READ_CARD.replace("blast_radius: read", "blast_radius: godmode")
        card = write_card(bad)
        env = {**os.environ, "MICROWAVE_SHADOW": "1"}
        r = subprocess.run([sys.executable, str(GATES / "gate_schema.py"), str(card)],
                           capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)  # not blocking
        self.assertIn("SHADOW", r.stdout + r.stderr)

    def test_run_gates_respects_shadow_end_to_end(self):
        # the hook path is run_gates -> gates; shadow must survive the whole chain
        import os
        bad = VALID_READ_CARD.replace("blast_radius: read", "blast_radius: godmode")
        card = write_card(bad)
        env = {**os.environ, "MICROWAVE_SHADOW": "1"}
        r = subprocess.run([sys.executable, str(GATES / "run_gates.py"), str(card)],
                           capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)  # hook path not blocking


class TestGateTestableRefs(unittest.TestCase):
    def test_rejects_a_check_naming_a_nonexistent_gate(self):
        import tempfile
        root = Path(tempfile.mkdtemp())
        (root / "wiki").mkdir()
        (root / "wiki" / "INDEX.md").write_text("# idx\n", encoding="utf-8")
        (root / "gates").mkdir()
        agents = root / "wiki" / "agents"
        agents.mkdir()
        card = agents / "ghost-ref.md"
        card.write_text(GHOST_GATE_CARD, encoding="utf-8")
        rc, out = run_gate("gate_testable.py", card)
        self.assertEqual(rc, 1, out)
        self.assertIn("does not exist", out)


sys.path.insert(0, str(GATES))
import gate_slop  # noqa: E402


class TestSlopBlanking(unittest.TestCase):
    """gate_slop's citation-blanking: a banned word in prose is scanned, but the
    same word inside a code fence / inline code / blockquote is blanked first, so
    citing slop to talk about it never trips the gate."""

    def test_prose_keeps_the_word(self):
        self.assertIn("delve", gate_slop._blank_quoted("we delve here"))

    def test_fence_is_blanked(self):
        self.assertNotIn("delve", gate_slop._blank_quoted("p\n```\ndelve\n```\n"))

    def test_inline_code_is_blanked(self):
        self.assertNotIn("delve", gate_slop._blank_quoted("a `delve` b"))

    def test_blockquote_is_blanked(self):
        self.assertNotIn("delve", gate_slop._blank_quoted("> delve here"))

    def test_blanking_preserves_line_count(self):
        # the offsets in a slop report must stay accurate: blank, don't delete
        src = "one\n```\ntwo\nthree\n```\nfour\n"
        self.assertEqual(gate_slop._blank_quoted(src).count("\n"), src.count("\n"))


FED_CARD = """---
type: agent-card
kind: service
name: Invoice Parser
slug: invoice-parser
status: staging
blast_radius: read
mission: parse invoices and extract line totals from pdfs
definition_path: flows/invoice-parser.md
owner: "@me"
synonyms: []
brief:
  success_criteria:
    - "totals match (check: a test sums line items and compares)"
  volume_cap: 10 files per run
  abort_conditions: stop if a path escapes the target folder
---

# Invoice Parser

Reads PDFs. Writes nothing.
"""

FED_AGENT_LINE = ("- [agent] invoice-parser: parse invoices and extract line "
                  "totals from pdfs → flows/invoice-parser.md\n")


class TestFederatedIndex(unittest.TestCase):
    """A card overlapping an agent that lives ONLY in a federated repo must be
    caught, and the hit must name the repo that already holds it. Without the
    federation manifest, the same card is green: proof it is federation, not the
    local registry, doing the catching."""

    def _local_with_card(self, federated=None):
        local = repo_with_index("# Registry index\n")  # no agent lines locally
        agents = local / "wiki" / "agents"
        agents.mkdir()
        card = agents / "invoice-parser.md"
        card.write_text(FED_CARD, encoding="utf-8")
        if federated is not None:
            (local / ".microwave").mkdir()
            (local / ".microwave" / "federation").write_text(
                str(federated) + "\n", encoding="utf-8")
        return local, card

    def test_no_manifest_is_local_only(self):
        import federated_index
        local = repo_with_index("- [agent] a: x → p\n- [agent] b: y → q\n")
        lines = federated_index.federated_index_lines(local)
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(src is None for src, _ in lines))

    def test_manifest_tags_foreign_lines_with_repo_name(self):
        import federated_index
        fed = repo_with_index(FED_AGENT_LINE)
        local, _ = self._local_with_card(federated=fed)
        foreign = [(s, l) for s, l in federated_index.federated_index_lines(local)
                   if s is not None]
        self.assertEqual(len(foreign), 1)
        self.assertEqual(foreign[0][0], fed.name)

    def test_absent_federated_repo_is_skipped_not_fatal(self):
        import federated_index
        local, _ = self._local_with_card(federated=Path(tempfile.mkdtemp()) / "gone")
        lines = federated_index.federated_index_lines(local)  # must not raise
        self.assertTrue(all(src is None for src, _ in lines))

    def test_self_reference_in_manifest_is_excluded(self):
        import federated_index
        local = repo_with_index("- [agent] a: x → p\n")
        (local / ".microwave").mkdir()
        (local / ".microwave" / "federation").write_text(
            str(local) + "\n", encoding="utf-8")  # points at itself
        lines = federated_index.federated_index_lines(local)
        self.assertEqual(len(lines), 1)  # not doubled

    def test_antidup_catches_cross_repo_duplicate(self):
        fed = repo_with_index(FED_AGENT_LINE)
        _, card = self._local_with_card(federated=fed)
        rc, out = run_gate("gate_antidup.py", card)
        self.assertEqual(rc, 1, out)
        self.assertIn(fed.name, out)  # the message names the repo holding the dup

    def test_antidup_green_without_federation(self):
        _, card = self._local_with_card(federated=None)
        rc, out = run_gate("gate_antidup.py", card)
        self.assertEqual(rc, 0, out)


CONTEXT_CARD = """---
type: agent-card
kind: context
name: My Repo Guard
slug: my-repo-guard
status: staging
blast_radius: read
repo: my-repo
mission: guard the my-repo repository and drive its conventions
definition_path: flows/my-repo-guard.md
owner: "@me"
synonyms: [my-repo, guard]
uses: [copywriter]
brief:
  success_criteria:
    - "loads repo conventions (check: a test asserts the card names the repo)"
  volume_cap: 1 per repo
  abort_conditions: stop if the repo path is missing
---

# My Repo Guard

## Interfaces

Reads the repo. Writes nothing.
"""


class TestTaxonomy(unittest.TestCase):
    def test_missing_kind_fails(self):
        bad = VALID_READ_CARD.replace("kind: service\n", "")
        rc, out = run_gate("gate_schema.py", write_card(bad))
        self.assertEqual(rc, 1)
        self.assertIn("kind", out)

    def test_bad_kind_fails(self):
        bad = VALID_READ_CARD.replace("kind: service", "kind: sidekick")
        rc, out = run_gate("gate_schema.py", write_card(bad))
        self.assertEqual(rc, 1)

    def test_context_without_repo_fails(self):
        bad = CONTEXT_CARD.replace("repo: my-repo\n", "")
        rc, out = run_gate("gate_schema.py", write_card(bad, slug="my-repo-guard"))
        self.assertEqual(rc, 1, out)
        self.assertIn("repo", out)

    def test_context_with_repo_passes(self):
        rc, out = run_gate("gate_schema.py",
                           write_card(CONTEXT_CARD, slug="my-repo-guard"))
        self.assertEqual(rc, 0, out)


class TestGateUses(unittest.TestCase):
    def _card_in(self, index_body, card_text=CONTEXT_CARD, name="my-repo-guard"):
        root = repo_with_index(index_body)
        agents = root / "wiki" / "agents"
        agents.mkdir()
        card = agents / f"{name}.md"
        card.write_text(card_text, encoding="utf-8")
        return card

    def test_uses_resolves_to_service(self):
        card = self._card_in(
            "- [service] copywriter: writes copy → wiki/agents/copywriter.md\n")
        rc, out = run_gate("gate_uses.py", card)
        self.assertEqual(rc, 0, out)

    def test_uses_missing_service_fails(self):
        card = self._card_in("- [service] other: x → p\n")  # no copywriter
        rc, out = run_gate("gate_uses.py", card)
        self.assertEqual(rc, 1, out)
        self.assertIn("copywriter", out)

    def test_uses_pointing_at_a_context_does_not_resolve(self):
        # only [service] lines satisfy uses; a [context] slug does not
        card = self._card_in("- [context] copywriter: x → p\n")
        rc, out = run_gate("gate_uses.py", card)
        self.assertEqual(rc, 1, out)

    def test_no_uses_is_green(self):
        card = self._card_in("- [service] copywriter: x → p\n",
                             card_text=VALID_READ_CARD, name="test-reader")
        rc, out = run_gate("gate_uses.py", card)
        self.assertEqual(rc, 0, out)


if __name__ == "__main__":
    unittest.main()
