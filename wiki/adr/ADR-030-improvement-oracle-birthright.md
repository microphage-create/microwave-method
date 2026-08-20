---
type: adr
id: ADR-030
title: Self-improvement is a birthright; the done-criteria are the oracle
status: proposed
date: 2026-08-20
scope: meta
author: microwave + microphage-create
---

# ADR-030: Self-improvement is a birthright; the done-criteria are the oracle

## Context

The two-plane self-improvement loop (ADR-029) is not specific to the method: any
governed agent has a source (its card and definition) and runs on a real estate,
so the same loop applies. But a loop only improves what it can measure. The
method improves reliably because it has an unusually good progress oracle almost
for free: tests, gates, "the estate still passes", and the devil. Most targets do
not. Copying the duplication-and-sync mechanism to a new agent without a
trustworthy progress signal produces churn, or worse, optimizes the proxy instead
of the goal.

## Decision

Every governed agent's executable done-criteria are its **improvement oracle**:
the pass/fail signal `flows/improve.md` reads to decide a change actually
improved it. Self-improvement is therefore a birthright of every agent the
factory makes, and the oracle is mandatory: `gate_testable` already rejects a
hollow check, so the factory refuses to create an agent that has no signal to
improve toward. The hard part of improving anything is the oracle, not the
duplication; the factory enforces the hard part rather than pretending it is
free.

## Consequences

Easier: any agent becomes improvable through the same loop, with no per-agent
plumbing. Harder: a creator must state a real, executable success signal at
creation, not a vibe; a domain with no measurable success is a domain the loop
cannot safely improve, and that is surfaced at creation instead of discovered
later. Forbidden: shipping a self-improving agent whose oracle is a check that
would pass on a broken agent (Goodhart bait).

## Links

[[ADR-029-self-improvement-loop]] [[ADR-002-machine-gates]] [[ADR-009-devil-review]]
