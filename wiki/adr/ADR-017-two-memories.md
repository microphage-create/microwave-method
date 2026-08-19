---
type: adr
id: ADR-017
title: Two memories, method distills, work accumulates and never does
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-017: Two memories, method distills, work accumulates and never does

## Context

The anti-gas-factory pass (RULES.md, ADRs archived when distilled) risks a
dangerous misread: that the framework wants LESS documentation. The
opposite is its whole point. The purpose is total capture of work: in a
2000-person org where 100 people touch one feature, the system must record
each contribution, who did it, what, why, and how, like humans in a
company but automated. The confusion is that "method docs" and "work docs"
were treated the same.

## Decision

There are two memories, governed oppositely:

- **Method memory** (how the system itself works: rules, method ADRs,
  scope: meta). It DISTILLS: once a decision is in `RULES.md` and enforced
  in code, its ADR is archived. The method footprint stays small so nobody
  reads a library to act.
- **Work memory** (what was produced and why: project ADRs, learnings,
  bugs, session-saves, devil-reports, scope: a project). It ACCUMULATES
  and is never distilled or pruned. It is append-only and attributed:
  every atom carries its author (agent and human) and its rationale. This
  is the collective logbook, the value, the git-blame-with-the-why.

The two-plane wiki already separates them (meta vs product plane, ADR-005):
this rule states that distillation applies to the meta plane ONLY. The
product plane grows without limit, on purpose.

## Consequences

Method stays light; work stays complete. A feature touched by a hundred
people has a hundred attributed traces, reconstructable by author, time,
and reason. Capture is maximal where it is the product (work) and minimal
where it is overhead (method). Cost: the product plane can be large; it is
plain markdown, searchable, and that size IS the asset.

## Links

[[ADR-005-two-plane-wiki]] [[ADR-012-session-saves]]
