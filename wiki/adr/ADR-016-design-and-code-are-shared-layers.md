---
type: adr
id: ADR-016
title: Design and code conventions are shared layers governed by conformance gates
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-016: Design and code conventions are shared layers governed by conformance gates

## Context

An agent ecosystem also produces UI and code. If each agent invents its
own components and its own coding style, that is sprawl in another
dimension: the product becomes illegible, the codebase inconsistent. The
question is how the framework governs design and code without a dedicated
agent policing every commit.

## Decision

Design and code conventions are SHARED LAYERS (ADR-015 forms), not agents:

- The **design system is a data-source WITH the wiki's compound loop**:
  tokens, components and patterns in a machine-readable index (the
  `llms.txt` / registry pattern). It is not read-only. An agent producing
  UI (1) reads it FIRST and reuses before inventing (component anti-dup),
  (2) stages what it newly produces, (3) the gatekeeper promotes it into
  the canonical DS or points back to the existing component. Every UI
  build can enrich the DS, exactly as every work session enriches the
  wiki: produce, curate, promote. Homogeneity is the by-product of
  anti-dup plus governed promotion, not of discipline.
- **Coding conventions are doctrine**: style, patterns, forbidden
  constructs, injected into any agent that writes code.

Conformance is machine, not meeting:

- `gate_design`: a produced component conforms to the design-system
  data-source (uses its tokens) AND is not a duplicate of an existing one
  (component anti-dup before it may be staged for promotion)
- `gate_code`: produced code conforms to the coding doctrine (lint,
  patterns, banned constructs)

Both are the `gate_slop` pattern applied to UI and code: a defect is
rejected before activation, with an actionable message. The rules banks
are pluggable per organization; the mechanism ships, the org's DS and
conventions plug in (proprietary ones stay private, like the slop bank).

## Consequences

Design and code stop being per-agent free choices and become read-from-a-
layer, checked-by-a-gate. The two-plane wiki now holds agents, ADRs, the
design-system data-source, and the coding doctrine: one governed context,
many consumers. Cost: the org must express its DS as data and its
conventions as checkable rules; a DS that is only a Figma file cannot be
consumed by agents until it has a machine-readable layer.

## Links

[[ADR-015-artifacts-have-a-form]] [[ADR-011-anti-slop]] [[ADR-005-two-plane-wiki]]
