---
type: adr
id: ADR-015
title: Artifacts have a form, the factory reshapes and does not just register
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-015: Artifacts have a form, the factory reshapes and does not just register

## Context

The first adopt REX scanned a whole estate as "skills" and tried to merge
them as if all were agents. One of them was not an agent at all: a
personal wiki, a data source read by several agents. Treating it as an
agent to merge would have destroyed a shared layer. An estate mixes forms;
calling everything an agent is a category error that the framework must
prevent, not commit.

## Decision

Every artifact has a FORM, and the adopt scan classifies it before
proposing a disposition:

- **agent**: it acts, has a blast radius, creates or modifies (the
  registry's citizens)
- **data-source**: a wiki, KB, vault, index; it is READ by agents (lives
  in the wiki layer, ADR-005; never a registry agent)
- **tool**: a function or library an agent calls (referenced, not
  registered as an agent)
- **doctrine**: rules or context injected into agents (a shared context
  layer)

A fifth adopt disposition joins migrate/merge/keep-as-is/retire:
**reshape**: the artifact is in the wrong form; move it to the right one
(a wiki masquerading as a skill becomes a data-source in the wiki layer;
an agent that is only a function becomes a tool). The factory chooses the
most adapted form and how it is best consumed; it does not just wrap
whatever shape it found.

## Consequences

Merges, duplication checks and blast-radius reasoning apply to agents;
data-sources are governed as shared layers (LRN-007); tools and doctrine
are referenced. The registry stops conflating forms, which is what let the
sprawl hide. Cost: the scan must judge form, a harder call than counting
files; the devil and the gatekeeper are the backstop when it is ambiguous.

## Links

[[ADR-005-two-plane-wiki]] [[ADR-010-adopt-first]]
