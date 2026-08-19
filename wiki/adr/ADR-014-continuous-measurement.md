---
type: adr
id: ADR-014
title: The system measures itself, prevention is counted at the source
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-014: The system measures itself, prevention is counted at the source

## Context

The value of governing agents is mostly invisible: the duplicate never
created, the leak never committed, the defect caught before activation, the
context not rediscovered. That is exactly the "opaque cost" Gartner names as
the top cause of agentic-project abandonment. A benefit nobody can point at
gets cut. Estimating it is dishonest ("we don't estimate, we instrument");
but instrumentation only works if the invisible event is recorded WHEN it
happens, because prevention leaves no trace by default.

## Decision

Governance events are logged to an append-only ledger
(`wiki/metrics/LEDGER.md`) at the moment they occur:

- `created` when an agent activates (with `created_in_minutes` from its card)
- `intercepted` when a gate or a devil round rejects a defect before
  activation (with the source and severity)
- `deduped` when a creation is blocked as a duplicate
- `purged` when an agent or atom is retired

`gates/metrics.py` aggregates the ledger deterministically (stdlib, no LLM)
into a report: agent surface, method cost, and above all the interception
count, which is the invisible benefit made visible. `flows/metrics.md` is
the ritual: read it at each gatekeeper session and before/after any
sanitation wave, so the "is it better now" question is answered by the
ledger, not by feeling. Vanity metrics are forbidden by the consumption
test: a number that no decision consumes is not logged.

## Consequences

Prevention becomes a counter, and ROI becomes a before/after diff of two
ledger reports rather than an opinion. The honest limit is stated in the
report: reuse and compute savings need the operator's provider dashboard;
the ledger measures what the loop itself can see.

## Links

[[ADR-002-machine-gates]] [[ADR-009-devil-review]] [[ADR-012-session-saves]]
