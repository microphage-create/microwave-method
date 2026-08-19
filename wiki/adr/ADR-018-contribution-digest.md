---
type: adr
id: ADR-018
title: A per-author contribution digest that counts work, never judges people
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-018: A per-author contribution digest that counts work, never judges people

## Context

Because work memory is attributed (ADR-017) and the ledger records
created / intercepted / deduped / purged, the system can produce a daily
per-person digest: "today alice created 3 agents; bob's card was
intercepted at the devil". Powerful for a large org: transparency
of who moves the product. But a system that judges people gets sabotaged:
if capture serves to rank and punish, people stop capturing honestly or
game the counter (Grudin's law, the very failure the manifesto cites).

## Decision

`gates/metrics.py --digest` aggregates the ledger BY AUTHOR into factual
contribution counts. Two hard boundaries, in the tool and in doctrine:

- It reports CONTRIBUTIONS (created, intercepted, deduped, purged),
  attributed and neutral. It never emits a verdict on a person ("good",
  "bad").
- The data is for transparency, recognition, and learning. Turning it into
  a ranking to punish is an out-of-band use that poisons adoption; the
  framework does not provide the ranking and warns against it.

Every ledger line gains an optional 5th field, the author (agent + human).

## Consequences

A daily logbook of attributed work exists for a hundred-people feature.
Whether it becomes recognition or a tribunal is a management choice the
framework refuses to make for you, and warns is a survival question:
a scoreboard that punishes empties itself.

## Links

[[ADR-017-two-memories]] [[ADR-014-continuous-measurement]]
