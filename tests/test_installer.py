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
        self.assertTrue((tmp / "CLAUDE.md").is_file() and (tmp / "AGENTS.md").is_file())
        self.assertTrue((tmp / "wiki" / "agents" / "microwave.md").is_file())
        self.assertFalse(list(tmp.rglob("*.pyc")), "shell install must not ship bytecode")
        self.assertIn("agent zero", (tmp / "wiki" / "INDEX.md").read_text(encoding="utf-8"))

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
