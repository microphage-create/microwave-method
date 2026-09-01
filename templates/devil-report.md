---
type: devil-report
artifact: path/or/slug/of/the/attacked/artifact
result: CLEAN
rounds: 0
progression: []
date: YYYY-MM-DD
---

# Devil report: {artifact}

## Result

CLEAN | FAILED | STALLED. {rounds} rounds, progression {[N] → [M] → [0]}.

## Rounds

### Round 1
- Provisioning: {access granted · re-provisioning events · claims ruled
  RIGHTLY REFUSED, with reasons; "default" when nothing special. A round
  replaced after re-provisioning keeps its entry AND its round number,
  retitled `### Round N (replaced: re-provisioned)`; the fresh entry is
  `### Round N`. The `progression` array records one count per round
  number: the final verdict's, never the replaced one's.}
- Facts: {V verified · C contradicted · U unverifiable}
  - {claim → verified|contradicted|unverifiable → how, one line per claim}
- Objections: {K kills | H high | M medium}
  - [severity] {objection, one line}
  - {for a "no further bypass found" on a criterion: the transports and
    bypass classes actually attempted, one line}
- Fixes applied: {one line per fix}

### Round 2
...

## Recurring objections

{Objections that survived a fix attempt: learning candidates for the wiki.}

## Gatekeeper note

{Filled by the gatekeeper at judgment: accepted / rejected and why.}
