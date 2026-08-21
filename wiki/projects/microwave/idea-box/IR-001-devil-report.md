---
type: devil-report
artifact: IR-001 installer-seeds-scaffold (flows/save.md fresh-install fix)
result: CLEAN
rounds: 4
progression: [2, 2, 2, 0]
date: 2026-08-21
---

# Devil report: IR-001 installer-seeds-scaffold

## Result

CLEAN. 4 rounds, progression [2] → [2] → [2] → [0]. The count held at 2 for
three rounds but was not a stall: each round attacked a different, deeper
layer (approach choice, then introduced regressions, then a byte-level
subtlety), and no fixed objection ever reappeared.

## Rounds

### Round 1 (on the first, rejected approach: a Step 0 in flows/save.md)
- Objections: 2 medium
  - [MEDIUM] legend drift: Step 0 restated the register/ledger legend, diverging from the canonical files.
  - [MEDIUM] un-pinned second copy of the legend in flow prose, free to drift.
- Fix applied: abandoned the prose approach. Root cause is the installer not
  seeding the scaffold (it already seeds INDEX). Reverted flows/save.md; moved
  the fix into all three installers, pinned by the parity test.

### Round 2 (on the installer approach)
- Objections: 2 medium
  - [MEDIUM] uninstall asymmetry: WIKI_SPACES gained sessions/metrics but the dir-prune list did not, orphaning the two dirs (and failing the wiki rmdir).
  - [MEDIUM] the parity test pinned only a marker line per header, so unpinned prose could drift between install.sh and install.ps1.
- Fixes applied: added wiki/sessions + wiki/metrics to the prune list before
  wiki; strengthened the test to pin the whole header block; added a test that
  a clean uninstall leaves no orphan wiki dirs.

### Round 3
- Objections: 2 medium
  - [MEDIUM] byte-parity across the 3 seed sites is not guaranteed (ps1 emits CRLF per .gitattributes) and the content-parity test cannot see it.
  - [MEDIUM] the shell seed of the two new files had no execution coverage (sh end-to-end asserted only INDEX).
- Fixes applied: added REGISTER/LEDGER existence+content asserts to the sh
  end-to-end test. For the EOL point: decided NOT to normalize (platform-native
  CRLF/LF is inert, pre-existing from the INDEX seed, and out of scope for
  seeding); documented the content-parity contract in the test and IR-001.

### Round 4
- Objections: 0. All eight surfaces swept clear; the EOL decision confirmed
  defensible (no concrete failing scenario); the test guards confirmed
  load-bearing (they fire red on a broken seed/prune). CLEAN.

## Recurring objections

None survived a fix. The EOL point raised in round 3 was resolved by a
reasoned decision + documentation, not a code change, and round 4 confirmed it
as clear rather than re-raising it.

## Gatekeeper note

Accepted by Marcel ("fait tout") and merged via PR #10. The CLEAN loop and the
live dogfood of both shell installers were the basis; the EOL non-fix was
reviewed and judged defensible, not a defect.
