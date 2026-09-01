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
   artifact, not in intentions or replies. The orchestrator PROVISIONS each
   devil: read-only access to the artifact, the registry index, the
   protocol, and the estate the artifact's claims are about (the paths,
   mounts and credentials in reach). Provisioning grants least privilege
   and READ-ONLY only, never a write or prod-mutating credential: a
   credential that cannot be granted read-only is not granted at all. A
   claim the devil reports `unverifiable (access)` is a provisioning
   failure of the orchestrator: fix the provisioning and re-run the round;
   it is never fixed by editing the artifact and never held against it.
   ONE re-provisioning attempt per claim, total; a re-run replaces its
   round's VERDICT, never its report entry (both entries stay, the first
   marked `replaced (re-provisioned)`), and never advances the round count
   or the stagnation clock. The artifact is FROZEN between a round and its
   re-run, and the re-run inherits the replaced round's non-access findings
   verbatim into its verdict: the fresh devil newly judges only the
   access-blocked claims, then appends - re-provisioning buys access, never
   a free fix-attack cycle. If access still cannot be granted, or granting
   it would itself be unsafe, the orchestrator rules the claim RIGHTLY
   REFUSED, with the reason on record. Grants die with the round: whatever
   access was provisioned is revoked when the round's verdict lands,
   nothing accumulates across rounds. The PROVISIONING RECORD is the one
   context hand-off from orchestrator to fresh devil, and it carries
   exactly three kinds of line, nothing else: the access granted; the
   claims already ruled RIGHTLY REFUSED, with reasons (the devil fires the
   protocol's row 2b from the safety-relevant ones among these, and files
   nothing for the ordinary ones); and whether a previous round's fix
   DROPPED a safety claim instead of making it verifiable, in which case
   the devil's surface-2 sweep must ask whether the vanished guard was
   load-bearing.
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
