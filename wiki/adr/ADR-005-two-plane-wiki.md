---
type: adr
id: ADR-005
title: One wiki format, two scopes, governed promotion
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-005: One wiki format, two scopes, governed promotion

## Context

Org knowledge and project knowledge have different audiences but identical
mechanics. Two systems double maintenance; one flat space rots.

## Decision

One atom format (typed frontmatter, wikilinks, one line in INDEX), two
scopes: meta plane (`wiki/agents/`, `wiki/adr/`) and product plane
(`wiki/projects/<name>/`). Subsidiarity: atoms live at the lowest sufficient
level. Promotion upward happens only through the gatekeeper, via `_staging/`,
with traced kills.

## Consequences

A single toolchain (gates, index) serves both planes. The registry index is
the junction: it indexes agents AND points into project wikis.

## Links

[[ADR-002-machine-gates]]
