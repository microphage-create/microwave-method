---
type: learning
id: LRN-009
title: The design system enriches itself like the wiki, homogeneity is a by-product
date: 2026-08-19
scope: microwave
---

# LRN-009: The design system is a compound memory

## What happened

The gatekeeper pushed the design-system-as-data-source idea one step
further: it is not read-only. Each agent that produces CSS or a component
adds something, and those somethings must stay homogeneous across agents.

## Why (root cause)

A read-only DS fossilizes (every agent reinvents) or, with no gate, bloats
into chaos (five different buttons). Homogeneity cannot be asked of
agents; it must be produced by the same forces that keep the wiki clean.

## How to apply

Give the DS the wiki's compound loop (ADR-016): before producing UI, an
agent runs component anti-dup against the DS; what it newly produces is
staged; the gatekeeper promotes it into the canonical DS or redirects to
the existing component. `gate_design` enforces token conformance and
non-duplication. The thesis holds for CSS: the more UI you produce, the
smarter the DS gets, instead of the more illegible.

## Links

[[ADR-016-design-and-code-are-shared-layers]] [[ADR-012-session-saves]]
