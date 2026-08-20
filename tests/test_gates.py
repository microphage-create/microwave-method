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

    def test_short_id_matches_on_boundary_not_substring(self):
        root = Path(tempfile.mkdtemp())
        d = root / "wiki" / "projects" / "x" / "learnings"
        d.mkdir(parents=True)
        (root / "wiki" / "INDEX.md").write_text("# idx\n", encoding="utf-8")
        (d / "LRN-1.md").write_text("# one\nalpha\n", encoding="utf-8")
        # the only mention anywhere is 'LRN-10', which must NOT reheat 'LRN-1'
        (d / "LRN-10.md").write_text("# ten\nsee LRN-10\n", encoding="utf-8")
        git = ["git", "-C", str(root)]
        subprocess.run(git + ["init", "-q"], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["-c", "user.email=t@t", "-c", "user.name=t",
                              "commit", "-qm", "seed"], check=True)
        sys.path.insert(0, str(GATES))
        import decay
        names = {Path(s["atom"]).name for s in decay.find_stale(root, 0.0)}
        self.assertIn("LRN-1.md", names)  # 'LRN-10' is not a reference to 'LRN-1'


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

FED_AGENT_LINE = ("- [service] invoice-parser: parse invoices and extract line "
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
        local = repo_with_index("- [service] a: x → p\n- [service] b: y → q\n")
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
        local = repo_with_index("- [service] a: x → p\n")
        (local / ".microwave").mkdir()
        (local / ".microwave" / "federation").write_text(
            str(local) + "\n", encoding="utf-8")  # points at itself
        lines = federated_index.federated_index_lines(local)
        self.assertEqual(len(lines), 1)  # not doubled

    def test_malformed_manifest_degrades_not_fatal(self):
        import federated_index
        root = repo_with_index("- [service] a: x → p\n")
        (root / ".microwave").mkdir()
        # a directory where the manifest file belongs: read must fail cleanly
        (root / ".microwave" / "federation").mkdir()
        lines = federated_index.federated_index_lines(root)  # must not raise
        self.assertTrue(all(src is None for src, _ in lines))

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

    def test_shipped_template_kind_is_clean(self):
        # the YAML subset does not strip inline comments, so 'kind: service # x'
        # would pollute the value; the shipped template must parse to a real enum.
        sys.path.insert(0, str(GATES))
        from _lib import read_frontmatter
        root = Path(__file__).resolve().parent.parent
        fm, _ = read_frontmatter(root / "templates" / "agent-card.md")
        self.assertIn(fm.get("kind"), {"context", "service"})

    def test_template_has_no_inline_map(self):
        # the YAML subset cannot parse inline {..} maps; the template must not
        # teach a palette form that fails when a user uncomments it.
        root = Path(__file__).resolve().parent.parent
        text = (root / "templates" / "agent-card.md").read_text(encoding="utf-8")
        self.assertNotIn("palette: {", text)

    def test_service_with_repo_fails(self):
        bad = VALID_READ_CARD.replace("kind: service", "kind: service\nrepo: some-repo")
        rc, out = run_gate("gate_schema.py", write_card(bad))
        self.assertEqual(rc, 1, out)
        self.assertIn("repo", out)

    def test_arrow_in_mission_fails(self):
        bad = VALID_READ_CARD.replace("read files and report what they contain",
                                      "read files → report what they contain")
        rc, out = run_gate("gate_schema.py", write_card(bad))
        self.assertEqual(rc, 1, out)


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


class TestActivate(unittest.TestCase):
    def test_index_line_carries_the_kind_token(self):
        import activate
        self.assertEqual(
            activate.index_line("service", "copywriter", "writes copy"),
            "- [service] copywriter: writes copy → wiki/agents/copywriter.md")
        self.assertNotIn("[agent]", activate.index_line("context", "suez", "guards"))

    def test_status_flip_tolerates_trailing_whitespace(self):
        import activate
        text, n = activate.STATUS_FLIP_RE.subn("status: active",
                                               "status: staging   \n", count=1)
        self.assertEqual(n, 1)
        self.assertIn("status: active", text)

    def test_status_flip_tolerates_quotes(self):
        # gate_schema strips quotes, so 'status: "staging"' is a valid enum; the
        # flip must match it too, or a green card cannot be activated.
        import activate
        for raw in ('status: "staging"\n', "status: 'staging'\n", "status: staging\n"):
            _, n = activate.STATUS_FLIP_RE.subn("status: active", raw, count=1)
            self.assertEqual(n, 1, raw)


class TestSlopSeverity(unittest.TestCase):
    """Opinionated style rules warn (never block); objective defects still block.
    Uses the real shipped slop-rules.csv, so a reclassification regression trips."""

    def _scan(self, text):
        import gate_slop
        root = Path(__file__).resolve().parent.parent
        rules = gate_slop.load_rules(root)
        p = Path(tempfile.mkdtemp()) / "x.md"
        p.write_text(text, encoding="utf-8")
        return gate_slop.scan(p, rules)  # (rejects, warns)

    def test_em_dash_warns_not_blocks(self):
        rejects, warns = self._scan("a — b\n")
        self.assertFalse(rejects, "em-dash must not block")
        self.assertTrue(warns, "em-dash should still warn")

    def test_dive_warns_not_blocks(self):
        # 'deep dive' / 'dive into' is the sibling tell of 'delve'; warn, not block
        rejects, warns = self._scan("Let's deep dive into the module.\n")
        self.assertFalse(rejects, "dive must not block")
        self.assertTrue(warns, "deep dive should warn")

    def test_plain_prose_without_dive_is_clean(self):
        # control: ordinary prose must not trip the new rule
        rejects, warns = self._scan("The module parses the file and returns totals.\n")
        self.assertFalse(warns, "clean prose must not warn on the dive rule")

    def test_placeholder_still_blocks(self):
        rejects, _ = self._scan("Lorem ipsum dolor\n")
        self.assertTrue(rejects, "a leftover placeholder is an objective defect")

    def test_as_an_ai_still_blocks(self):
        rejects, _ = self._scan("As an AI, here is the answer.\n")
        self.assertTrue(rejects, "assistant leakage is an objective defect")


class TestScanEstate(unittest.TestCase):
    def _estate(self):
        root = Path(tempfile.mkdtemp())
        a = root / "my-app"
        (a / ".git").mkdir(parents=True)
        (a / "package.json").write_text("{}", encoding="utf-8")
        (a / "next.config.js").write_text("", encoding="utf-8")
        b = root / "my-api"
        (b / ".git").mkdir(parents=True)
        (b / "pyproject.toml").write_text("", encoding="utf-8")
        (root / "not-a-repo").mkdir()  # no .git: must be ignored
        return root

    def test_finds_only_git_repos(self):
        import scan_estate
        names = {r.name for r in scan_estate.find_repos(self._estate())}
        self.assertEqual(names, {"my-app", "my-api"})

    def test_detects_stack_per_repo(self):
        import scan_estate
        stacks = {c["repo"]: c["stack"]
                  for c in scan_estate.propose(self._estate())["contexts"]}
        self.assertIn("Next.js", stacks["my-app"])
        self.assertIn("Python", stacks["my-api"])

    def test_proposes_one_context_per_repo_plus_services(self):
        import scan_estate
        plan = scan_estate.propose(self._estate())
        self.assertEqual(len(plan["contexts"]), 2)
        self.assertTrue(all(c["slug"] for c in plan["contexts"]))
        self.assertTrue(plan["services"])

    def test_slug_collision_is_flagged(self):
        import scan_estate
        root = Path(tempfile.mkdtemp())
        for name in ("my-app", "my_app"):  # both slugify to 'my-app'
            (root / name / ".git").mkdir(parents=True)
        plan = scan_estate.propose(root)
        self.assertEqual(scan_estate._duplicate_slugs(plan["contexts"]), ["my-app"])


class TestJsoncStrip(unittest.TestCase):
    """The Windows adapter rewrites the user's settings.json; stripping trailing
    commas must not reach inside string values (silent corruption)."""

    def test_string_interior_preserved_trailing_comma_removed(self):
        import json
        adapters = Path(__file__).resolve().parent.parent / "embodiment" / "adapters"
        sys.path.insert(0, str(adapters))
        import windows
        src = '{"a": "Solarized, ]", "b": [1, 2,], }'
        d = json.loads(windows._strip_jsonc(src))
        self.assertEqual(d["a"], "Solarized, ]")  # comma+bracket inside a string kept
        self.assertEqual(d["b"], [1, 2])           # a real trailing comma dropped


EMBODIED_STAGING_CARD = """---
type: agent-card
kind: service
name: test-body
slug: test-body
status: staging
blast_radius: write
mission: sorts and moves files and logs what it changed
definition_path: flows/test-body.md
owner: "@me"
synonyms: [writer, body, mover]
embodiment:
  display_name: test-body
  icon: embodiment/icons/test-body.png
  palette:
    bg: "#14181a"
    fg: "#e6ebeb"
    accent: "#7f93a8"
  embodied: false
brief:
  success_criteria:
    - "the change is logged (check: a test greps the log for today's date)"
  volume_cap: 10 files per run
  abort_conditions: stop if a path escapes the target folder
---

# test-body

## Interfaces

Writes moved files under the target folder and logs each change.
"""


class TestGateEmbodiment(unittest.TestCase):
    """Regression: the pre-commit hook copies the staged card into a bare tmp
    dir (no repo above it) and runs the per-file gates on it. gate_embodiment
    must locate the repo root via cwd there, or NO embodied agent can ever be
    committed. write_card() reproduces that exact tmp-dir layout."""

    def test_embodied_card_in_tmpdir_does_not_crash_on_repo_root(self):
        rc, out = run_gate("gate_embodiment.py",
                           write_card(EMBODIED_STAGING_CARD, slug="test-body"))
        self.assertNotIn("cannot locate repo root", out)
        self.assertEqual(rc, 0, out)

    def test_read_only_bodiless_card_in_tmpdir_passes(self):
        # a bodiless read card must also survive the tmp-dir root lookup
        rc, out = run_gate("gate_embodiment.py", write_card(VALID_READ_CARD))
        self.assertNotIn("cannot locate repo root", out)
        self.assertEqual(rc, 0, out)


class TestGateSlopRoot(unittest.TestCase):
    """A single file passed on the command line may live outside any repo; the
    gate must fall back to cwd for the rules bank, like its sibling gates, not
    crash on 'cannot locate repo root'."""

    def test_out_of_tree_file_falls_back_to_cwd(self):
        p = Path(tempfile.mkdtemp()) / "note.md"
        p.write_text("The parser reads the file and returns totals.\n", encoding="utf-8")
        rc, out = run_gate("gate_slop.py", p)
        self.assertNotIn("cannot locate repo root", out)
        self.assertEqual(rc, 0, out)


class TestEmbodyDeadShell(unittest.TestCase):
    """embody warns when an agent is embodied with no launch: the profile opens
    a terminal but invokes nothing (a dead shell). Pure helper, no machine touch."""

    def _embody(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "embodiment"))
        import embody
        return embody

    def test_no_launch_returns_a_note(self):
        note = self._embody().dead_shell_note("", "ops")
        self.assertIsNotNone(note)
        self.assertIn("ops", note)
        self.assertIn("launch", note)

    def test_launch_set_is_silent(self):
        self.assertIsNone(self._embody().dead_shell_note("claude", "ops"))


if __name__ == "__main__":
    unittest.main()
