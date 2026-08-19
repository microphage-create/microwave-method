# Flow: metrics (read the ROI, log the invisible)

The system measures itself so "is it better now" is answered by the ledger,
not by feeling (ADR-014). Two halves: logging (continuous) and reading
(ritual).

## Logging (happens inside other flows, do not skip)

Append one line to `wiki/metrics/LEDGER.md`, `DATE | event | subject |
detail | author` (author = agent+human, ADR-018), the moment it occurs:

- appended by `flows/save.md` at session end: `created | <slug> |
  <minutes> | <author>` (from the card's `created_in_minutes`)
- in `devil-loop` / gates, on every rejection before activation:
  `intercepted | <slug> | <source>:<severity>` (source = gate name or
  `devil-rN`). This is the line that turns a prevented defect into a
  counted benefit; without it the benefit is invisible forever.
- in `adopt` / manual purge: `purged | <slug> | <why> | <author>`
- on an anti-dup block: `deduped | <slug> | <matched> | <author>`

## Reading (ritual)

At each gatekeeper session, and BEFORE and AFTER any sanitation wave:

```
python gates/metrics.py                 # full report
python gates/metrics.py --since <date>  # a window
python gates/metrics.py --digest        # per-author contribution digest
```

ROI is a before/after diff of two reports: run it before a cleanup, run it
after, compare. The interception count is the invisible benefit; the agent
surface and method cost are the visible ones.

## The honest boundary

The ledger measures what the loop can see. Reuse rate and token/compute
savings live in your provider's usage dashboard: pull them there,
before/after adoption, and cite YOUR numbers, never an estimate. Vanity
metrics are banned by the consumption test: if a number changes no
decision, do not log it.
