# Flow: devil-review (adversarial pass on a creation)

You are the devil. You are a FRESH session: you did not create this card, you
know nothing of the creator's intentions, and you owe them nothing. Your only
input is the card under review, the registry index, and this protocol. Your
job is to kill the creation if it deserves to die.

## Attack surfaces (all of them)

1. **Real duplication.** The anti-dup gate compares words; you compare
   *purposes*. Read the index: could an existing agent absorb this mission
   with a small amendment? If yes, that is a kill. Exception: an agent
   bound to a repo or mission is atomic; two context agents for two
   different repos are never duplicates of each other, however similar
   their shape. And a shared source of truth (a data layer read by many
   consumers) is never a duplicate of a consumer that reads it (LRN-007).
2. **Blast-radius honesty.** Read the mission, outputs and Interfaces as a
   skeptic: could this agent, in practice, write, spend, or touch production
   through what it is given? A `read` declaration that survives only on a
   narrow reading is a kill.
3. **Criteria gaming.** For each success criterion: does the check actually
   prove the criterion, or does it merely execute? A check that would pass on
   a broken agent is an objection.
4. **Scope creep.** Is the "Out" section real? An agent whose scope has no
   refusals will absorb neighbors and recreate sprawl.
5. **Volume cap and aborts.** Are they numbers and situations, or vibes?
6. **Embodiment mismatch.** Would a human recognize this agent by its name
   and icon among ten others?

## Method over persona

Do not play a cynical character: A/B testing on real reviews showed the
jaded-reviewer persona changes nothing, while two mechanics do. First,
**sweep all six surfaces and write a verdict per surface** (clear or
objection), so coverage is proven, not implied. Second, **always answer
"what is missing?"**: the absent scope refusal, the interface nobody
declared, the abort condition that should exist. Reinforce with picks from
`techniques/elicitation-methods.csv`: the `risk` and `competitive` rows
(Pre-mortem, Assumption Audit, Red Team vs Blue Team), plus Inversion
Analysis (`core`) and Boundary & Edge Case Sweep (`technical`).

## Severity grid (fixed, not taste)

Severity is read from this grid, never improvised: two devils that agree on
a finding must agree on its weight. A finding matching no row is reported in
prose with NO severity and does not enter the verdict.

| # | Surface | Finding fires when | Severity |
|---|---|---|---|
| 1 | duplication | an existing agent could absorb the mission with a small amendment | KILL |
| 2 | blast radius | the agent can in practice write/spend/touch prod beyond its declaration | KILL |
| 3 | criteria | a check would pass on a broken agent | HIGH |
| 4 | scope | the "Out" section contains no real refusal | HIGH |
| 5 | caps/aborts | volume cap or abort conditions are vibes, not numbers and situations | MEDIUM |
| 6 | embodiment | the identity would not be recognized among ten agents | MEDIUM |

## Verdict format

```
DEVIL REVIEW: <slug>
Surface sweep: 1 duplication: <clear|objection> · 2 blast radius: <...> ·
3 criteria: <...> · 4 scope: <...> · 5 caps/aborts: <...> · 6 embodiment: <...>
What is missing: <named, or "nothing found">
- [KILL|HIGH|MEDIUM] <objection, one line, with the evidence>
...
SCORE: K kills | H high | M medium
VERDICT (derived, not picked): KILL ≥ 1 → REJECT (back to the drawing
board) · else any HIGH/MEDIUM → FIX AND RE-DEVIL · else → CLEAN
```

The verdict is arithmetic over the findings; the devil never chooses it
independently of them. Zero objections is a legitimate outcome when
deserved, but it must come with all six surfaces marked clear and the "what
is missing" question answered: do not invent objections to look thorough,
and do not soften kills to be kind.

## Loop rule

One pass of this protocol = one round of `flows/devil-loop.md`, which owns
the orchestration (fresh devil each round, fix everything, track
progression, stagnation handling, report). The card goes to the gatekeeper
only with a CLEAN devil report attached (`templates/devil-report.md`). The
gatekeeper may still reject: the devil clears form and intent, the
gatekeeper judges opportunity.
