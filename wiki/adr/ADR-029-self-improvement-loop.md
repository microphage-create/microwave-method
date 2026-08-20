---
type: adr
id: ADR-029
title: Self-improvement loop and federated idea-box
status: proposed
date: 2026-08-20
scope: meta
author: microwave + microphage-create
---

# ADR-029: Self-improvement loop and federated idea-box

## Context

The maintainer of Microwave rarely runs Microwave on a real, messy estate. The
`gate_embodiment` crash that blocked every embodied-agent commit was invisible
in the source repo and its tests; it surfaced only when the framework was
installed and dogfooded on a real ecosystem (activating the first embodied
agent). The agent that installs and drives an install is therefore the best
source of product signal, because it is at once the user and the mechanic. Every
client's install hits frictions the source never sees, and each finding is
useful to every other install.

## Decision

1. **The install is the source's proving ground.** Framework code (gates,
   flows, hooks, templates, techniques, slop, the embodiment engine) is owned by
   the source and pushed one-way into an install; the install's estate (`wiki/`,
   `.git/`, `.claude/`, `embodiment/icons/`) is never overwritten
   (`dev-loop/sync.py`). Framework changes are made in the source, synced,
   dogfooded on the real estate, and only then shipped. Never edit the framework
   directly in an install.

2. **Improvement signals are captured as scrubbed reports (the idea-box).** A
   bug hit, a friction, or an idea becomes a structured local report: the
   abstract pattern only (what broke, in what shape), never the client's data.

3. **Federation is opt-in and scrubbed.** An install MAY, only on explicit
   opt-in, publish its scrubbed reports to a central repo. The central
   aggregates and homogenizes (dedup, cluster, rank) them; installs MAY pull the
   ranked ideas. What leaves a machine is the shape of a problem, never agent
   names, paths, missions, or content. This is the archive rule (never capture a
   secret) applied to outbound telemetry.

4. **Inbound ideas are hypotheses, not patches.** An idea pulled from the
   network is gated by the same loop as any local change: test, dogfood, then
   gatekeeper, before it ships. It is never auto-applied. A shared idea-box
   without this gate is a supply-chain vector.

## Consequences

Easier: collective learning with a network effect; a fix found on one estate
reaches all. Harder: it requires a scrubbing layer, a consent model, and a
homogenization step, none of them free. Forbidden: auto-collecting client data,
and auto-applying network ideas to the framework.

Roadmap, built in order, each shippable alone: (a) the local idea-box (100%
on-machine, no network); (b) an opt-in, scrubbed upstream publish; (c) central
aggregation and pull. Only (a) is in scope until the data model and consent of
(b) are defined. The existing `federated_index.py` and `.microwave/federation`
manifest are the reuse point for (b)/(c), not a fresh mechanism.

## Links

[[ADR-010-adopt-first]] [[ADR-002-machine-gates]] [[ADR-009-devil-review]]
