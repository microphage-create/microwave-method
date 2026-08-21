# Flow: improve (continuous-improvement mode)

Microwave improves itself the way it improves anything: by dogfooding. An
install is the source's proving ground (ADR-029). This flow runs the loop that
turns a friction hit on a real estate into a shipped framework fix, without ever
letting an unverified change reach the product.

## The two planes, never crossed

- **SOURCE** is the product repo (the framework's home). Framework code is
  edited here, never in an install.
- **INSTALL** is a live Microwave on a real estate. It receives framework code
  one-way through an install-local sync tool (`dev-loop/sync.py`, estate-
  preserving, set up per install, not shipped in the distribution) and is where a
  change is dogfooded on real data.

Edit in the source, sync into the install, dogfood, then ship. A change edited
directly in an install is reverted by the next sync: that is the reminder, not a
bug.

## The idea-box

Every friction, bug, or idea worth acting on becomes one
`templates/improvement-report.md` under `wiki/projects/microwave/idea-box/`. It
records the SHAPE of the problem, never the estate's data: no agent names,
paths, missions, or content. A report is the unit of work this flow consumes,
and the unit that federation (ADR-029, opt-in and scrubbed) would one day
publish. The scrubbing is not optional: it is what makes a report safe to share.

## One cycle

1. **Pick** one item: an idea-box report, or a friction hit right now.
2. **Change** it in the SOURCE, on a branch. Smallest change that resolves it.
3. **Verify at the source**: `python -m unittest discover tests`, and the gates
   the change touches. A bug fix ships with a regression test that fails without
   it.
4. **Sync** into the install with your install-local sync tool (e.g. `python
   dev-loop/sync.py --check`, which you set up per install). The check must report
   the estate still healthy: a framework change that breaks the real estate is a
   failed cycle, not a ship.
5. **Dogfood**: exercise the changed behavior on the real estate. Test a few
   agents, confirm the registry is consistent and everything is indexed and
   saved (`gate_wiki`). Watch what actually changed.
6. **Adversary**: for a change to `gates/`, `flows/`, `hooks/` or a rule, run
   `flows/devil-loop.md`. An idea, whether local or pulled from the network, is
   a hypothesis until an adversary fails to kill it.
7. **Commit + push** the source branch and open a PR. Never commit the
   framework straight to the default branch.
8. **Ship gate**: this is the mode boundary below.
9. **Close the report** in the idea-box and start the next.

## Modes

The mode sets ONE thing: who closes step 8. It never lowers the bar of steps
3-6; those run identically in both.

### Semi-auto (default)

The loop runs autonomously through the PR. It STOPS at the merge and the
release: the human is the gatekeeper of every ship. Autonomy on the work,
human on the consequence. This is the default and the recommended mode for a
product other people install.

### Full-auto (opt-in, guarded, default OFF)

The loop also merges its own PR and publishes, WITHOUT a human, but only inside
hard rails. It is the highest-stakes capability in the system: a release reaches
every install. It runs only when ALL of these hold, and refuses otherwise:

- **Explicit arming**: the file `.microwave/full-auto` exists in the source and
  names the allowed scope. Picking the menu is not enough; arming is a separate,
  deliberate act.
- **Scope allowlist**: bug fixes and their tests only. NEVER a new flow, gate,
  adapter, rule, ADR, a dependency, a breaking change, or a public-API change.
  Anything outside the allowlist falls back to semi-auto and waits.
- **Green everything**: `unittest` all pass, every gate green, `devil-loop`
  CLEAN, and the install's post-sync `--check` healthy. One red anywhere aborts
  the ship and leaves the PR open for the human.
- **Kill switch**: deleting `.microwave/full-auto` disarms immediately, mid-run.
- **Trace**: every full-auto ship writes an idea-box report of what shipped and
  why it was in scope, so the human can audit after the fact.

Full-auto is a convenience for the narrow, boring, well-tested fixes. The moment
a change is interesting, it is out of scope by definition and the human decides.

## Never

- Never ship a change that failed step 3, 4, 5 or 6, in either mode.
- Never auto-apply an idea pulled from the network without running it through
  this whole cycle.
- Never widen the full-auto allowlist from inside a full-auto run.
