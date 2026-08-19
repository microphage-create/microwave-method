"""Regression net for the installer's auto-launch security guard.

_resolve_agent is the fix for the Windows RCE where shutil.which('claude')
prepends the CWD, so a claude binary planted at a repo's root would be launched
by 'uvx microwave-method'. These tests pin that a binary resolving INSIDE the
target is refused, and one OUTSIDE is allowed. A refactor that drops the guard
turns these red.
"""
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
        base = Path(__file__).resolve().parent
        target = base / "some_target_repo"          # need not exist
        outside = base / "real_claude"              # sibling, outside target
        microwave_method.shutil.which = lambda _: str(outside)
        trusted, refused = microwave_method._resolve_agent(target)
        self.assertEqual(trusted, outside.resolve())
        self.assertIsNone(refused)

    def test_no_agent_on_path(self):
        microwave_method.shutil.which = lambda _: None
        trusted, refused = microwave_method._resolve_agent(Path("."))
        self.assertIsNone(trusted)
        self.assertIsNone(refused)


if __name__ == "__main__":
    unittest.main()
