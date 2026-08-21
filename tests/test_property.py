"""Property-based tests for the hand-rolled parsers in gates/_lib.py.

An optional dev layer (borrowed from pydantic's use of Hypothesis): it runs when
`hypothesis` is installed and skips cleanly otherwise, so the base suite stays
stdlib-only-runnable. CI installs hypothesis so this layer always runs there.

The invariant it guards: the YAML-subset parser (and its helpers) must be TOTAL
over their input type. For ANY input they return a value or raise GateError, a
controlled failure the gates translate into an actionable message. They must
never leak an uncontrolled exception (IndexError, RecursionError, ValueError):
malformed frontmatter must fail loud-but-clean, never crash the gate. The parser
is provably robust today; this keeps it that way across future edits.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "gates"))
from _lib import GateError, _scalar, get, parse_yaml_subset

try:
    from hypothesis import given, settings
    from hypothesis import strategies as st
    HAS_HYPOTHESIS = True
except ImportError:  # optional dev layer
    HAS_HYPOTHESIS = False


# The @given/@settings decorators are evaluated at class-definition time, so the
# whole thing lives behind the import guard; without hypothesis a stub reports
# the skip and the stdlib-only base suite stays green.
if HAS_HYPOTHESIS:
    # a line strategy mixing pure noise with frontmatter-shaped lines and deep
    # indentation / nesting, to exercise the indentation stack and the inline-list
    # scalar path, not just random text the parser ignores.
    _line = st.one_of(
        st.text(alphabet="abc :-[]{},#\t\"'", max_size=30),
        st.from_regex(r"[ ]{0,20}- [a-z_]+:.*", fullmatch=True),
        st.from_regex(r"[ ]{0,20}[a-z_]+: \[.*\]", fullmatch=True),
        st.builds(lambda n: " " * n + "- x:", st.integers(0, 40)),
    )

    class TestParserRobustness(unittest.TestCase):
        @settings(max_examples=1500, deadline=None)
        @given(st.lists(_line, max_size=40))
        def test_parse_returns_dict_or_gateerror(self, lines):
            try:
                self.assertIsInstance(parse_yaml_subset(lines), dict)
            except GateError:
                pass  # a controlled, actionable failure is allowed

        @settings(max_examples=1500, deadline=None)
        @given(st.text(max_size=60))
        def test_scalar_never_crashes_uncontrolled(self, s):
            try:
                _scalar(s)
            except GateError:
                pass

        @settings(max_examples=1000, deadline=None)
        @given(
            st.dictionaries(st.text(max_size=5), st.none() | st.text() | st.integers()),
            st.text(max_size=15),
        )
        def test_get_never_crashes(self, d, dotted):
            # navigating an arbitrary dict by a dotted path always returns
            # something, never raises: get() is the safe accessor the gates use.
            get(d, dotted)

else:

    class TestParserRobustness(unittest.TestCase):
        @unittest.skip("hypothesis not installed (property tests are an optional dev layer)")
        def test_property_layer(self):
            pass


if __name__ == "__main__":
    unittest.main()
