"""Regression net for the installer's auto-launch security guard.

_resolve_agent is the fix for the Windows RCE where shutil.which('claude')
prepends the CWD, so a claude binary planted at a repo's root would be launched
by 'uvx microwave-method'. These tests pin that a binary resolving INSIDE the
target is refused, and one OUTSIDE is allowed. A refactor that drops the guard
turns these red.
"""
import sys
import unittest
from pathlib import Path

import microwave_method


class ResolveAgent(unittest.TestCase):
    def setUp(self):
        self._orig_which = microwave_method.shutil.which

    def tearDown(self):
        microwave_method.shutil.which = self._orig_which

    def test_refuses_binary_inside_target(self):
        target = Path(__file__).resolve().parent
        planted = target / "claude_planted"  # resolves inside target
        microwave_method.shutil.which = lambda _: str(planted)
        trusted, refused = microwave_method._resolve_agent(target)
        self.assertIsNone(trusted)
        self.assertEqual(refused, planted.resolve())

    def test_allows_binary_outside_target(self):
        import tempfile
        target = Path(tempfile.mkdtemp())                   # a target repo, off cwd
        outside = Path(tempfile.mkdtemp()) / "real_claude"  # off both target and cwd
        microwave_method.shutil.which = lambda _: str(outside)
        trusted, refused = microwave_method._resolve_agent(target)
        self.assertEqual(trusted, outside.resolve())
        self.assertIsNone(refused)

    def test_no_agent_on_path(self):
        microwave_method.shutil.which = lambda _: None
        trusted, refused = microwave_method._resolve_agent(Path("."))
        self.assertIsNone(trusted)
        self.assertIsNone(refused)


class ShellInstall(unittest.TestCase):
    def _require_bash(self):
        # A *working* bash, not just one on PATH: on Windows the name resolves to
        # the WSL launcher, which fails if no distro is installed.
        import subprocess
        try:
            probe = subprocess.run(["bash", "-c", "echo ok"],
                                   capture_output=True, text=True)
        except (OSError, ValueError):
            self.skipTest("bash not available")
        if probe.returncode != 0 or probe.stdout.strip() != "ok":
            self.skipTest("no working bash (WSL stub or broken shell)")

    def test_install_sh_end_to_end(self):
        import subprocess
        import tempfile
        self._require_bash()
        repo = Path(__file__).resolve().parent.parent
        tmp = Path(tempfile.mkdtemp())
        subprocess.run(["git", "-C", str(tmp), "init", "-q"], check=True)
        r = subprocess.run(["bash", str(repo / "install" / "install.sh"), str(tmp)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((tmp / "flows" / "welcome.md").is_file())
        self.assertTrue((tmp / "CLAUDE.md").is_file())
        self.assertFalse((tmp / "AGENTS.md").exists(), "Claude Code is the only harness (ADR-032)")
        self.assertTrue((tmp / "wiki" / "agents" / "microwave.md").is_file())
        self.assertFalse(list(tmp.rglob("*.pyc")), "shell install must not ship bytecode")
        self.assertIn("agent zero", (tmp / "wiki" / "INDEX.md").read_text(encoding="utf-8"))
        # the session scaffold is born with the install, so the first save can run
        reg = tmp / "wiki" / "sessions" / "REGISTER.md"
        led = tmp / "wiki" / "metrics" / "LEDGER.md"
        self.assertTrue(reg.is_file() and led.is_file(), "sh install must seed the scaffold")
        self.assertIn("Session save register", reg.read_text(encoding="utf-8"))
        self.assertIn("Governance ledger", led.read_text(encoding="utf-8"))
        # the /microwave front door must ship on the shell path too (parity with uvx)
        self.assertTrue((tmp / ".claude" / "commands" / "microwave.md").is_file(),
                        "sh install must ship .claude/commands so /microwave exists")

    def test_install_sh_does_not_run_target_planted_hooks(self):
        # RCE guard, shell path: a repo can ship its own hooks/ (git never
        # auto-installs them). Microwave must wire the hook from its trusted
        # source, never execute or install the target's copy.
        import subprocess
        import tempfile
        self._require_bash()
        repo = Path(__file__).resolve().parent.parent
        tmp = Path(tempfile.mkdtemp())
        subprocess.run(["git", "-C", str(tmp), "init", "-q"], check=True)
        (tmp / "hooks").mkdir()
        marker = tmp / "PWNED"
        payload = f"#!/usr/bin/env bash\ntouch '{marker.as_posix()}'\n"
        (tmp / "hooks" / "install-hooks.sh").write_text(payload, encoding="utf-8")
        (tmp / "hooks" / "pre-commit").write_text(payload, encoding="utf-8")
        r = subprocess.run(["bash", str(repo / "install" / "install.sh"), str(tmp)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertFalse(marker.exists(),
                         "install ran a target-planted hook script (RCE)")
        wired = tmp / ".git" / "hooks" / "pre-commit"
        self.assertTrue(wired.is_file(), "the Microwave hook was not wired")
        trusted = (repo / "hooks" / "pre-commit").read_bytes()
        self.assertEqual(wired.read_bytes(), trusted,
                         "wired hook is not the trusted one (target pre-commit slipped in)")


class SeedConsistency(unittest.TestCase):
    def test_agent_zero_index_line_in_all_three_installers(self):
        # the INDEX seed lives in 3 places (WIKI_INDEX + install.sh + install.ps1);
        # a divergence would mean a shell-installed repo has a different registry
        root = Path(__file__).resolve().parent.parent
        line = ("- [service] microwave: agent zero, the desktop front door that "
                "opens a context-loaded session on this repo")
        sh = (root / "install" / "install.sh").read_text(encoding="utf-8")
        ps = (root / "install" / "install.ps1").read_text(encoding="utf-8")
        py = (root / "microwave_method" / "__init__.py").read_text(encoding="utf-8")
        self.assertIn(line, sh)
        self.assertIn(line, ps)
        self.assertIn("- [service] microwave: agent zero", py)
        self.assertIn("wiki/agents/microwave.md", py)

    def test_session_scaffold_seed_in_all_three_installers(self):
        # REGISTER + LEDGER headers are seeded by all three installers so a fresh
        # install can run its first save (IR-001). Pin a distinctive line of each
        # across the three seed sites: a divergence would seed a drifted scaffold.
        from microwave_method import WIKI_LEDGER, WIKI_REGISTER
        root = Path(__file__).resolve().parent.parent
        sh = (root / "install" / "install.sh").read_text(encoding="utf-8")
        ps = (root / "install" / "install.ps1").read_text(encoding="utf-8")
        # pin the WHOLE header block (not a marker line) into both shell installers,
        # so no unpinned prose line can drift between install.sh and install.ps1.
        # This guards CONTENT parity; line endings are intentionally platform-native
        # (install.ps1 is `eol=crlf` per .gitattributes, install.sh is LF), and
        # read_text normalizes them, so the check is EOL-insensitive by design. The
        # seeded files are gate-skipped and read newline-agnostically everywhere.
        for blob in (sh, ps):
            self.assertIn(WIKI_REGISTER, blob)
            self.assertIn(WIKI_LEDGER, blob)
        # the seed matches the source's own canonical scaffold (fidelity): the live
        # files may append rows below the header, so pin the header as a prefix.
        canon_reg = (root / "wiki" / "sessions" / "REGISTER.md").read_text(encoding="utf-8")
        canon_led = (root / "wiki" / "metrics" / "LEDGER.md").read_text(encoding="utf-8")
        self.assertTrue(canon_reg.startswith(WIKI_REGISTER))
        self.assertTrue(canon_led.startswith(WIKI_LEDGER))


class UninstallSafety(unittest.TestCase):
    def test_uninstall_keeps_an_edited_file(self):
        import os
        import tempfile
        repo = Path(__file__).resolve().parent.parent
        tmp = Path(tempfile.mkdtemp())
        orig_payload = microwave_method._payload
        microwave_method._payload = lambda: repo
        os.environ["MICROWAVE_TARGET"] = str(tmp)
        os.environ["MICROWAVE_NO_LAUNCH"] = "1"
        try:
            sys.argv = ["mw"]
            microwave_method.main()  # install
            edited = tmp / "flows" / "welcome.md"
            self.assertTrue(edited.exists())
            edited.write_text("MY EDITS, keep me\n", encoding="utf-8")
            sys.argv = ["mw", "--uninstall"]
            microwave_method.main()  # uninstall
            self.assertTrue(edited.exists(), "uninstall must never delete an edited file")
            self.assertEqual(edited.read_text(encoding="utf-8"), "MY EDITS, keep me\n")
        finally:
            microwave_method._payload = orig_payload
            os.environ.pop("MICROWAVE_TARGET", None)
            os.environ.pop("MICROWAVE_NO_LAUNCH", None)
            sys.argv = ["mw"]

    def test_clean_uninstall_leaves_no_orphan_wiki_dirs(self):
        # a clean install then uninstall must prune every wiki space it created,
        # including the seeded sessions/ and metrics/, and wiki/ itself: adding a
        # space to WIKI_SPACES without a matching prune entry would orphan a dir.
        import contextlib
        import io
        import os
        import tempfile
        repo = Path(__file__).resolve().parent.parent
        tmp = Path(tempfile.mkdtemp())
        orig = microwave_method._payload
        microwave_method._payload = lambda: repo
        os.environ["MICROWAVE_TARGET"] = str(tmp)
        os.environ["MICROWAVE_NO_LAUNCH"] = "1"
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                sys.argv = ["mw"]
                microwave_method.main()  # install
                self.assertTrue((tmp / "wiki" / "sessions" / "REGISTER.md").exists())
                self.assertTrue((tmp / "wiki" / "metrics" / "LEDGER.md").exists())
                sys.argv = ["mw", "--uninstall"]
                microwave_method.main()  # uninstall (nothing edited)
            for orphan in ("wiki/sessions", "wiki/metrics", "wiki"):
                self.assertFalse((tmp / orphan).exists(),
                                 f"clean uninstall left an orphan dir: {orphan}")
        finally:
            microwave_method._payload = orig
            os.environ.pop("MICROWAVE_TARGET", None)
            os.environ.pop("MICROWAVE_NO_LAUNCH", None)
            sys.argv = ["mw"]

    def test_uninstall_keeps_an_edited_codeowners(self):
        import contextlib
        import io
        import os
        import tempfile
        repo = Path(__file__).resolve().parent.parent
        tmp = Path(tempfile.mkdtemp())
        orig = microwave_method._payload
        microwave_method._payload = lambda: repo
        os.environ["MICROWAVE_TARGET"] = str(tmp)
        os.environ["MICROWAVE_NO_LAUNCH"] = "1"
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                sys.argv = ["mw"]
                microwave_method.main()
                co = tmp / "CODEOWNERS"
                # keep the placeholder, add a real rule (the natural mid-setup state)
                co.write_text(co.read_text(encoding="utf-8") + "\ndocs/ @marcel-edited\n",
                              encoding="utf-8")
                sys.argv = ["mw", "--uninstall"]
                microwave_method.main()
            self.assertTrue(co.exists(), "uninstall must keep an edited CODEOWNERS")
            self.assertIn("@marcel-edited", co.read_text(encoding="utf-8"))
        finally:
            microwave_method._payload = orig
            os.environ.pop("MICROWAVE_TARGET", None)
            os.environ.pop("MICROWAVE_NO_LAUNCH", None)
            sys.argv = ["mw"]


class InstallPlan(unittest.TestCase):
    def test_dry_run_lists_files_no_bytecode_writes_nothing(self):
        import tempfile
        repo = Path(__file__).resolve().parent.parent
        tmp = Path(tempfile.mkdtemp())
        plan = microwave_method._install_plan(tmp, repo)
        self.assertGreater(len(plan), 20)  # flows, gates, templates, ...
        self.assertFalse([p for p in plan if p.suffix in (".pyc", ".pyo")],
                         "install plan must not carry bytecode")
        self.assertFalse([p for p in plan if "__pycache__" in p.parts],
                         "install plan must not carry __pycache__")
        self.assertFalse(list(tmp.rglob("*")), "dry-run must write nothing")

    def test_dry_run_matches_what_install_writes(self):
        import contextlib
        import io
        import os
        import tempfile
        repo = Path(__file__).resolve().parent.parent
        orig = microwave_method._payload
        microwave_method._payload = lambda: repo
        try:
            t1 = Path(tempfile.mkdtemp())
            plan = {str(p.relative_to(t1)) for p in microwave_method._install_plan(t1, repo)}
            t2 = Path(tempfile.mkdtemp())
            os.environ["MICROWAVE_TARGET"] = str(t2)
            os.environ["MICROWAVE_NO_LAUNCH"] = "1"
            with contextlib.redirect_stdout(io.StringIO()):
                sys.argv = ["mw"]
                microwave_method.main()
            written = {str(p.relative_to(t2)) for p in t2.rglob("*") if p.is_file()}
            self.assertEqual(plan, written, "dry-run must promise exactly what install writes")
        finally:
            microwave_method._payload = orig
            os.environ.pop("MICROWAVE_TARGET", None)
            os.environ.pop("MICROWAVE_NO_LAUNCH", None)
            sys.argv = ["mw"]


if __name__ == "__main__":
    unittest.main()
