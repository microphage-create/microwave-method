---
type: adr
id: ADR-020
title: Every change verifies its global impact before it lands
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-020: Every change verifies its global impact before it lands

## Context

The failure mode that quietly kills a governed system is the local fix
stacked on top of what already exists without checking the whole: a second
rule that contradicts the first, a fourth file for a job three files already
share, a patch that hides the problem under the rug instead of resolving it.
A local change blind to the global is a cigarette butt thrown in a forest:
each one is small, and the fire is certain. The framework already had this
instinct in pieces (gate_antidup checks the index before a creation, the
gatekeeper's conflict motif blocks a rule that fights an existing one, the
consumption test deletes a step nobody reads) but never named the principle
those pieces serve, so nothing enforced it for an ordinary edit.

## Decision

Every change, not just an agent creation, verifies its global impact before
it lands. Concretely, before adding or editing anything durable:

- Dedup and conflict-check against what already exists. If a rule, a file, or
  a concept already covers this, AMEND it; never stack a second one beside it.
  Distillation over accumulation (the anti-gas-factory rule) is this same law
  applied to doctrine.
- Name the vocabulary you touch. Three things must not end up called the same
  (see the index/register/ledger split in ADR-021): a change that reuses a
  loaded word without reconciling it is a collision waiting to happen.
- Leave the whole coherent, not just the diff correct. A green local edit that
  desyncs a neighbor is a regression, not a fix.

gate_antidup, the gatekeeper conflict motif, and the consumption test are
instances of this one rule, not separate ideas. New enforcement of it at
commit granularity is ADR-021 (a commit that lands an atom must name it, so
its global rationale is never lost).

## Consequences

The rule is stated once and the existing gates inherit their justification
from it instead of each re-arguing it. The honest limit: a machine can check
dedup, vocabulary collision, and index sync; it cannot fully check "leaves
the whole coherent". That judgment stays with the devil and the gatekeeper on
the full path, and with the author's discipline on the fast path. The rule
makes the expectation explicit; it does not pretend to automate all of it.

## Links

[[ADR-002-machine-gates]] [[ADR-009-devil-review]] [[ADR-021-traceability-is-a-git-projection]]
