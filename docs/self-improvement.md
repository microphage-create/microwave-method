# It improves itself

Microwave improves the way it asks you to improve anything it governs: by
dogfooding, with an adversary, in small reversible steps. This page is the
recipe, and the method applies it to itself first.

## Two planes, never crossed

- The **source** is the product: the framework's home, where its code is edited.
- An **install** is a live Microwave on a real estate. It receives framework code
  one way (`dev-loop/sync.py`, estate-preserving) and is where a change meets real
  data.

Edit in the source, sync into the install, dogfood, then ship. A change edited
directly in an install is reverted by the next sync: that is the reminder the two
planes are not the same, not a bug.

## One cycle

1. **Catch** a friction on real work and write it as one scrubbed
   improvement-report in the idea-box: the SHAPE of the problem, never the
   estate's data (no names, paths, or content). The scrubbing is what makes a
   report safe to share upstream one day (ADR-029).
2. **Fix** it in the source, on a branch, the smallest change that resolves it.
3. **Verify at the source**: the test suite, and the gates the change touches. A
   bug fix ships with a regression test that fails without it.
4. **Sync and dogfood**: push the change into the install and exercise it on the
   real estate; confirm the estate still passes its gates. A framework change that
   breaks a real estate is a failed cycle, not a ship.
5. **Adversary**: for a change to a gate, a flow, a hook, or a rule, run the devil
   loop (`flows/devil-loop.md`). A fresh session with no creation context tries to
   kill the change, and every objection is fixed before the next round. An idea is
   a hypothesis until an adversary fails to kill it.
6. **Ship, gated.** Semi-auto (the default) runs the whole cycle on its own but
   stops at the merge and the release: the human is the gatekeeper of every ship.
   Full-auto exists only inside hard rails (narrow bug fixes with tests, an
   explicit arming file, a kill switch) and refuses anything interesting.

Every step produces a reviewable, revertable unit: a branch, a PR, a single sync
commit. The worst case is `git revert`.

## Not just the method: every agent

Self-improvement is a birthright of every governed agent, not a feature bolted
onto the framework. Every agent has a source (its card and definition) and is
exercised on a real estate, so the same two-plane loop applies to it. This is the
second job of the executable done-criteria the factory demands: they are not only
the activation gate but the agent's improvement **oracle**, the pass/fail signal
the loop reads to know a change improved the agent instead of merely running. An
agent whose criteria are hollow can still activate, but it is unimprovable,
because the loop has no trustworthy signal to optimise toward. That is why
`gate_testable` refuses a filler check (ADR-030).

## The recipe, transferable

Strip the Microwave specifics and three things carry the autonomy:

- **A verifiable success criterion beats a vibe.** "Make it better" loops forever;
  "write the test that reproduces it, then make it pass" terminates. Turn every
  imperative into something a machine can check, and the agent can run to done.
- **The adversary is the quality engine, not the author.** The first attempt is
  often wrong; the value comes from an independent critic trying to kill it before
  it lands, not from being right the first time. Budget for the adversary.
- **Small, reversible, gated units.** One concern per change, a human at the ship,
  nothing irreversible without a yes. That is what makes autonomy safe to let run.

## Where it does not hold

Honesty, because the loop is not magic. It works here because verification is
cheap and objective: tests, gates, a dogfoodable install, a reversible release.
On pure taste, with no test and irreversible side effects, the same recipe is much
weaker, and the human has to stand closer. It also costs real compute: the
adversary rounds and the dogfooding are not free. The lesson to generalise is not
"trust the agent" but "invest in the verifiable criterion and the adversary before
you invest in the agent."
