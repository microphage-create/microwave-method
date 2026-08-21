# Flow: estate-guard (the convention-bringer for an estate)

The definition of the `estate-guard` service agent (`wiki/agents/estate-guard.md`).
It runs when someone points it at a folder of repositories and wants order imposed
on the sprawl. It does not gently propose; it DECLARES arbitrary house rules and
judges every repo against them. Read-only, always: it names the rule and the
verdict, it never moves, renames, writes, or deletes.

## When this runs

On demand: "look at my repos folder and lay down the rules", or as the second half
of onboarding an estate (scan_estate proposes the agents; this imposes the
organisation). Not a gate, not automatic.

## Steps

1. **Judge** the folder: run `python gates/estate_hygiene.py <folder>` (optionally
   `--stale-days N`). It declares the five house rules (R1 naming, R2 home, R3
   companion, R4 loose, R5 family) and emits a verdict per repo: rename to X, file
   under Y, or OK.
2. **Read the verdicts together**, worst-friction first: the misnamed repos, the
   stale ones bound for archive/, the doc companions to rename, the loose folders
   to fold or evict. Never a raw dump; the tool already names the rule each one
   breaks.
3. **Arbitrate the judgment calls the rules leave open**: is a stale repo dead or
   just paused? Is a split family (`claria` + `claria-site` + `claria-docs`) one
   project to consolidate, or a deliberate split to keep? The rules are arbitrary
   and firm; the human decides the few cases only they can.

## Done when

The human has the house rules, a verdict for every repo and loose folder, and the
target tree those verdicts produce, plus the list of renames and moves THEY will
make (the guardian lists them, the human runs them). Never a "done" that moved a
file.

## Never

Move, rename, write, or delete anything. Touch the code inside a repo. Run a rename
or a consolidation for the human. Bringing conventions is declaring the rules,
judging against them, and arbitrating the calls they leave open; the hands stay the
human's.
