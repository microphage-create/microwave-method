---
type: adr
id: ADR-001
title: One recursive method, two passes
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-001: One recursive method, two passes

## Context

Heavyweight methods charge full ceremony on every feature; plan-mode-style
planning leaves nothing durable. Method cost must amortize.

## Decision

One method, two passes. Pass 1, heavy, ONCE per agent: elicit, spec,
anti-dup, build, embody, register, seed. Pass 2, light, EVERY feature: intent,
short story with executable done-criteria, build, trace to wiki. No PRD in
pass 2: the agent card and the project wiki are the context.

## Consequences

Method cost is paid at agent creation and amortized across all its features.
The quality of pass 2 depends entirely on the quality of the card and wiki,
which is why pass 1 is gated.

## Links

[[ADR-002-machine-gates]] [[ADR-003-ceremony-selector]]
