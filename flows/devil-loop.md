# Flow: devil-loop (autonomous adversarial convergence)

The generic loop that hardens ANY artifact of the system until an adversary
finds nothing: agent cards, where it is the Devil guard of the full path in create-agent.md, stories before close,
rule amendments, releases. `flows/devil-review.md` defines one attack pass;
this flow defines the orchestration.

## The loop

```
produce → FRESH devil attacks → 0 objections ? → done (report attached)
              ▲                      no
              └── fix ALL objections ┘
```

Rules, all of them mandatory:

1. **Fresh eyes every round.** Each devil is a new session with no creation
   context and no memory of previous rounds. Fixes must live IN the
   artifact, not in intentions or replies.
2. **Fix everything.** Every objection (kill, high, medium) is addressed
   before the next round. No triage, no "later".
3. **No regressions.** A fixed objection that reappears is flagged and fixed
   first.
4. **Progression is tracked** in the report: `[7] → [3] → [1] → [0]`. If the
   count stagnates two rounds, change approach (restructure, do not patch).
   Three stagnations: stop, attach the report marked STALLED, escalate to
   the gatekeeper with the unresolved objections.
5. **Safety limit**: default 10 rounds. Reaching it marks the report
   FAILED; it is not an outcome.
6. **Zero is the only clean exit.** Not "acceptable with reservations."

## Report

Fill `templates/devil-report.md` as the loop runs. Consumers: the gatekeeper
(judges only artifacts with a clean report), and the project wiki (the
report is traced next to the artifact; recurring objections across loops are
learning candidates).

## When to run it

- Full-path agent creation: required. It is the Devil guard of create-agent.md.
- Stories whose done-criteria touch production: recommended before close.
- Rule amendments (`flows/amend-rule.md`): required before gatekeeper
  judgment.
- Anything the team is about to show outside: recommended.
