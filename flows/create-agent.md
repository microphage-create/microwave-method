# Flow: create-agent (Pass 1)

You are the factory, the single entry point for agent creation. The depth
is set by the agent's blast radius, not your mood (ADR-003). Two paths.

## Fast path (read-only agents): 3 steps, minutes

For an agent whose `blast_radius` is `read` (reads only, never writes,
spends, or touches production):

1. **Spec** the card (`templates/agent-card.md`). First set `kind` (ADR-028): a
   **context** agent guards one repo, so set `kind: context` and name it with
   `repo:`; a **service** is transversal and reusable, so `kind: service` and no
   `repo:`. Then: mission, I/O, the 3-section brief, done-criteria with executable
   checks, and `uses:` listing any services it calls (each must resolve). Write it
   to `wiki/_staging/<slug>.md`. Embodiment is OPTIONAL here (`embodied` may stay
   false): a throwaway read-only agent needs no desktop body.
2. **Gate**: `python gates/run_gates.py wiki/_staging/<slug>.md` (anti-dup,
   brief, schema, testable, embodiment, uses, slop, wiki, all bundled). Fix reds, re-run.
3. **Activate**: `python gates/activate.py wiki/_staging/<slug>.md`. Done,
   nobody to wait for.

That is the whole thing for the common case. The guards below apply ONLY
when the agent can do damage.

## Full path (write / spend / prod agents): the fast path plus guards

An agent that writes repos or data, spends money, or touches production
adds, around the three steps above:

- **Elicit** (before step 1): three anchors (invert: what makes it harmful
  or useless; neighbor: which agent is closest; scope cut: what is OUT),
  plus 2-3 techniques from `techniques/` if it helps. Feeds the spec, then
  discard.
- **Embody** (mandatory here, part of step 1): `python
  embodiment/embody.py wiki/_staging/<slug>.md`. A durable, powerful agent
  is recognizable on the desktop; the human validates the icon.
- **Build** (between spec and gate): create the agent definition at the
  card's `definition_path`.
- **Devil** (after the gates pass): a FRESH agent session with no creation
  context attacks the card via `flows/devil-review.md`, looped by
  `flows/devil-loop.md` until zero objections. The creator never reviews
  their own creation.
- **Gatekeeper** (replaces step 3's self-activation): runs `activate.py` as
  the act of judgment, clean devil report attached, or rejects (card stays
  in `_staging/`, marked `rejected`).
- **Seed** (after): create `wiki/projects/<domain>/` from
  `templates/project-seed.md` if the agent opens a new domain.

**When in doubt about blast radius, take the full path.** `gate_schema`
cross-checks a `read` declaration against write-signals, but the devil and
the gatekeeper are the real guard.

## The oracle: the done-criteria matter twice

An agent's executable done-criteria are not only the activation gate. They are
its **improvement oracle**: the pass/fail signal `flows/improve.md` reads to know
a change actually improved the agent and did not merely run. Self-improvement is
a birthright of every governed agent, not a bolt-on: an agent has a source (its
card and definition) and is exercised on a real estate, so the two-plane loop
that improves the method itself (ADR-030) applies to any agent the factory
makes. This is the second reason `gate_testable` rejects a hollow check: a weak
criterion still lets an agent activate, but it leaves the agent unimprovable,
because the loop would have no trustworthy signal to optimize toward. The hard
part of improving anything is the oracle, not the duplication; the factory
refuses to create an agent without one.
