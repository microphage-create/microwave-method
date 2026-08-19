# The method

The compact rule base is `wiki/RULES.md`: one line per rule, the what.
ADRs and learnings are archived rationale, the why, read on demand.
Doctrine distills into RULES.md and the code; it does not accumulate as
documents to read (the anti-gas-factory rule).


One recursive method applied to two types of objects (agents, features), tied
together by a registry. Not two stacked methods: one set of templates,
parameterized by what you create.

## Pass 0: adopting the existing estate (once, at install)

Run `flows/adopt.md`: point the framework at wherever your agents sleep
(`.claude/`, prompt folders, repos). Every artifact found gets a frozen
inventory entry in `wiki/_archive/`, and `wiki/_archive/BACKLOG.md` becomes
the shopping list of dispositions (migrate / merge / keep-as-is / reshape / retire).
Migrations are ordinary pass-1 creations seeded from their archive entry:
the cheapest creations you will ever run. Even before any migration, the
archive delivers the first promise of the method: the complete map of what
exists, which nobody had (ADR-010).

## Pass 1: creating an agent (once, depth by blast radius)

Run by `flows/create-agent.md`. The fast path is 3 steps; guards attach
only when the agent can do damage.

- **Fast path** (`read`): spec the card, run the gates, activate. Minutes,
  no human, body optional. That is the whole common case.
- **Full path** (`write|spend|prod`): the same 3 steps plus elicit,
  mandatory embodiment, build, a fresh-eyes devil loop until clean, and a
  human gatekeeper who activates or rejects.

The selector is the agent's power, never the creator's mood. If the fast
path grows past 3 steps, ceremony has crept in (see `wiki/RULES.md`).

## Pass 2: creating or improving a feature (light, every time)

Run by `flows/create-feature.md`. The agent is already contextualized: no PRD.

1. State the intent.
2. Write a short story (`templates/story.md`): 3-8 verifiable done-criteria,
   each tied to an executable check (`gate_testable` enforces it).
3. Build until checks pass.
4. Write traces to the project wiki (`templates/learning.md`, `templates/adr.md`,
   `templates/bug.md` as applicable) and update `wiki/INDEX.md`.

Improving a feature is lighter still: the ADRs and learnings are already in the
wiki; the agent starts from acquired knowledge, not from zero.

## Sessions: save and resume

Every working session ends with `flows/save.md`: one atomic batch (session
save with id `S-YYYYMMDD-NN-slug`, the session's untraced atoms, the
register line in `wiki/sessions/REGISTER.md`), validated by the gates
before it counts, persisted in one commit. Any session on any machine
resumes it later with `flows/resume.md` and the id alone. Saves are the
ritual that feeds the wiki: the "Atoms produced: none, because..." line is
where compounding is won or lost (ADR-012).

## The wiki: one format, two scopes

- Meta plane (org-wide): `wiki/agents/` (cards), `wiki/adr/` (framework and
  org decisions), `wiki/INDEX.md` (the registry index: one line per artifact).
- Product plane (per project): `wiki/projects/<name>/` (brief, ADRs, learnings,
  bugs, sessions).
- `wiki/_staging/`: candidates awaiting judgment.

**Promotion (subsidiarity)**: an atom lives at the lowest level that suffices.
A project learning with cross-project value is moved to the meta plane by the
gatekeeper, never by its author. Kills are traced (the purge note stays in
`_staging/`, marked rejected, with a rationale).

## Instrumenting yourself

The method measures its own weight so the middle stays a property, not a
promise:

- Log the wall-clock time of every pass-1 run (fast and full) in the agent card
  (`created_in_minutes`).
- Every quarter (or every N agents), run the consumption test on the method
  itself: list each artifact class and who consumed it. An artifact class with
  no consumer is removed from the flows by an amendment
  (`flows/amend-rule.md`).
- Token accounting: your provider's usage dashboard, filtered on agent
  sessions, before/after adoption. Do not trust our numbers; produce yours.
