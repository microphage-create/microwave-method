---
type: improvement-report
id: IR-001
title: first save on a fresh install writes into a non-existent scaffold
kind: bug
surface: flow
severity: blocks
status: open
scrubbed: true
date: 2026-08-21
source_signal: dogfood
---

# IR-001: first save on a fresh install writes into a non-existent scaffold

## The shape

`flows/save.md` reads `wiki/sessions/REGISTER.md` in Step 1 and appends to it
in Step 2, and appends to `wiki/metrics/LEDGER.md` in Step 2. On a fresh
install neither `wiki/sessions/` nor `wiki/metrics/` exists yet, so the very
first save has nothing to read and nowhere to append: it either fails or the
operator has to hand-create the two files with the right legend before the
flow can run. The flow assumes a scaffold that only a prior save produces, so
save N+1 works but save 1 does not.

## Reproduce

1. Install Microwave into a folder that has never run a save.
2. Run `/save`.
3. Step 1 reads `wiki/sessions/REGISTER.md`: absent. Step 2 appends to it and
   to `wiki/metrics/LEDGER.md`: both absent. The batch cannot complete without
   the operator seeding the two files by hand.

## Fix or idea

Seed the scaffold at install time, not at first save. The installer already
seeds `wiki/INDEX.md` from a constant if absent; do the same for
`wiki/sessions/REGISTER.md` and `wiki/metrics/LEDGER.md`, in all three
installers (the `uvx` package, `install.sh`, `install.ps1`), so a fresh
install is born with the scaffold and `flows/save.md` keeps no bootstrap
responsibility. Both filenames are in `gate_wiki`'s `SKIP_NAMES`, so seeded
files add no index obligation. Pin the three seed copies with the installer
parity test (`SeedConsistency`), the same guard that already pins the INDEX
seed, so the headers cannot drift across installers.

Accepted known property: the three installers emit platform-native line
endings (`install.ps1` writes CRLF per `.gitattributes eol=crlf`, the others
LF), inherited from the pre-existing INDEX seed. The scaffold files are
gate-skipped and read newline-agnostically everywhere, so this is inert;
forcing byte-identical EOL would touch the pre-existing INDEX seed and the
`.gitattributes` policy, out of scope for seeding the scaffold. The parity
test guards content, not EOL, by design.

Rejected alternative: a "Step 0" in `flows/save.md` that seeds on first save.
It patches the symptom (the checkpoint flow does not own estate bootstrap) and
duplicates the header legend into flow prose with no drift guard (devil round 1,
two MEDIUM findings). Seeding at install is the root fix.

## Ship

Branch `fix/save-seed-session-scaffold` on the source. Semi-auto: an installer
change is out of full-auto scope, so it stops at the PR for the human to merge.
Devil loop CLEAN in 4 rounds ([[IR-001-devil-report]]).
PR: https://github.com/microphage-create/microwave-method/pull/10 (awaiting merge).
