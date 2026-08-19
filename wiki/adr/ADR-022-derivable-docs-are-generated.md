---
type: adr
id: ADR-022
title: Derivable docs are generated views, gated for freshness (the README is a spreadsheet)
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-022: Derivable docs are generated views, gated for freshness (the README is a spreadsheet)

## Context

The most common rot in any repo is the README and the technical docs: things
are added, the doc is never updated. The reflex fix is an agent that resyncs
the doc periodically, but that treats the symptom and makes the truth depend on
an LLM that can itself drift or hallucinate, and it learns the drift a day
later. The real cause is the same one ADR-021 named: a doc that DESCRIBES the
repo's state is a second source of truth, hand-typed in parallel with the code.
Two sources for one truth desync by default. A doc section listing the gates,
the agents, the commands, is not prose, it is a derivable view written by hand,
which is precisely why it goes stale.

## Decision

Split docs by nature and treat each at its cause. A section that DESCRIBES
state is generated, never hand-typed. It lives between markers in the doc file;
`gates/docgen.py` fills it from the source of truth (for the gate table, the
`gate_*.py` docstrings and the run order), and `gate_docs.py` fails the commit
if the frozen text no longer equals what the formula produces. This is a
materialized view with a freshness gate: GitHub renders static text and runs no
formula on view, so the recalculation happens on WRITE (at commit), not on read.
The README becomes a spreadsheet, a formula plus a freshness check, not a
document to maintain.

A section that is NARRATIVE (the why, the vision, the tradeoffs) is not
generable, but it changes rarely, and when it does that change is a decision
(an ADR), which is exactly the commit where the narrative is edited too
(delivery is the save, ADR-019). An agent that rewrites narrative on a schedule
is a slop and re-litigation risk, and is refused. The only periodic role left
is to FLAG a narrative drift a gate cannot see, and the librarian already holds
that role (flagging rot); no new agent is added.

This is ADR-021's law applied to docs: a derivable artifact is a projection
generated on demand, never stored twice. docgen joins trace as a projection;
neither is "maintained".

## Consequences

The gate table cannot go stale: add a gate and the table regenerates itself
(gate_docs, added in this change, appeared in its own table). The tradeoff is
honest: a generated line is as good as the docstring it derives from, so the
guarantee text now lives in the gate, its single source; nuance that does not
derive (the slop bank is a starter, bring your own rows) stays as prose. New
generated sections are added by registering a generator and its markers; the
mechanism does not change. Adjacent doc files (docs/*.md) can carry markers the
same way when a section there proves derivable.

## Links

[[ADR-021-traceability-is-a-git-projection]] [[ADR-020-verify-global-impact]] [[ADR-019-capture-triggers-on-context-pressure]]
