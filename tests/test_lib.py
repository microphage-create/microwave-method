"""Unit tests for the YAML-subset parser in gates/_lib.py.

Stdlib unittest, no dependency (ADR-007). Run: python -m unittest discover tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "gates"))
from _lib import (GateError, _scalar, parse_yaml_subset,  # noqa: E402
                  get, tokenize, read_frontmatter)


class TestScalar(unittest.TestCase):
    def test_bare_string(self):
        self.assertEqual(_scalar("hello"), "hello")

    def test_quoted_keeps_inner_commas(self):
        self.assertEqual(_scalar('"a, b"'), "a, b")

    def test_int_and_negative(self):
        self.assertEqual(_scalar("42"), 42)
        self.assertEqual(_scalar("-7"), -7)

    def test_bool(self):
        self.assertIs(_scalar("true"), True)
        self.assertIs(_scalar("False"), False)

    def test_inline_list(self):
        self.assertEqual(_scalar("[a, b, c]"), ["a", "b", "c"])

    def test_inline_list_quoted_comma(self):
        self.assertEqual(_scalar('["a, b", c]'), ["a, b", "c"])

    def test_empty_inline_list(self):
        self.assertEqual(_scalar("[]"), [])

    def test_malformed_list_is_rejected_not_swallowed(self):
        # regression: a bare '[' with no closing ']' used to be kept as a string
        with self.assertRaises(GateError):
            _scalar("[a, b")


class TestParse(unittest.TestCase):
    def test_scalar_map(self):
        self.assertEqual(parse_yaml_subset(["a: 1", "b: two"]), {"a": 1, "b": "two"})

    def test_nested_map(self):
        self.assertEqual(parse_yaml_subset(["a:", "  b: 1"]), {"a": {"b": 1}})

    def test_block_list(self):
        self.assertEqual(parse_yaml_subset(["x:", "  - one", "  - two"]),
                         {"x": ["one", "two"]})

    def test_block_list_of_maps(self):
        self.assertEqual(parse_yaml_subset(["x:", "  - k: v"]),
                         {"x": [{"k": "v"}]})

    def test_comment_and_blank_lines_ignored(self):
        self.assertEqual(parse_yaml_subset(["# c", "", "a: 1"]), {"a": 1})

    def test_duplicate_key_rejected(self):
        with self.assertRaises(GateError):
            parse_yaml_subset(["a: 1", "a: 2"])

    def test_tab_indentation_rejected(self):
        with self.assertRaises(GateError):
            parse_yaml_subset(["a:", "\tb: 1"])

    def test_unparseable_line_rejected(self):
        with self.assertRaises(GateError):
            parse_yaml_subset(["not a mapping"])


class TestGet(unittest.TestCase):
    def test_nested_present(self):
        self.assertEqual(get({"a": {"b": 1}}, "a.b"), 1)

    def test_absent_returns_none(self):
        self.assertIsNone(get({"a": {}}, "a.b"))
        self.assertIsNone(get({}, "x"))

    def test_non_dict_midpath_returns_none(self):
        # 'a' is a scalar, so 'a.b' must not raise, it returns None
        self.assertIsNone(get({"a": 5}, "a.b"))


class TestTokenize(unittest.TestCase):
    def test_drops_stopwords(self):
        self.assertEqual(tokenize("the cat and the mat"), {"cat", "mat"})

    def test_lowercases(self):
        self.assertEqual(tokenize("Reader SCANNER"), {"reader", "scanner"})

    def test_drops_shorter_than_three(self):
        self.assertNotIn("ab", tokenize("ab cde"))


class TestReadFrontmatter(unittest.TestCase):
    def _write(self, text):
        p = Path(tempfile.mkdtemp()) / "f.md"
        p.write_text(text, encoding="utf-8")
        return p

    def test_parses_frontmatter_and_body(self):
        fm, body = read_frontmatter(self._write("---\na: 1\n---\n\nHello\n"))
        self.assertEqual(fm["a"], 1)
        self.assertIn("Hello", body)

    def test_crlf_frontmatter_parses(self):
        # a card authored on Windows must still parse (CR stripped, not kept)
        fm, _ = read_frontmatter(self._write("---\r\nslug: x\r\n---\r\nbody\r\n"))
        self.assertEqual(fm["slug"], "x")


if __name__ == "__main__":
    unittest.main()
