---
type: adr
id: ADR-011
title: Anti-slop gate with a pluggable rules bank
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-011: Anti-slop gate with a pluggable rules bank

## Context

Agents produce durable artifacts (wiki atoms, cards, docs) that read like
slop unless checked: em dashes, filler openers, buzzwords, hedging stacks,
placeholders. The proliferation of ungoverned skill packs on public
registries makes unedited LLM output the default quality level. Detection of
these tells is mechanical.

## Decision

`gates/gate_slop.py` scans durable artifacts (root docs, `docs/`, `flows/`,
`wiki/` except archive) against `slop/slop-rules.csv`: one row per rule
(regex, severity reject/warn, actionable message). The shipped bank is a
generic STARTER; organizations append or replace rows with their own
corpus. **Proprietary rule corpora stay private**: the framework ships the
mechanism, never an organization's rules. The gate runs in the card
pipeline, the pre-commit hook, and CI. Templates and imported technique
banks are excluded (placeholders and foreign wording are their point).

## Consequences

The first dogfood run rejected 74 em dashes in this repository's own files,
which is the proof the gate is needed. A rules bank is a blunt instrument:
it catches tells, not bad thinking; the devil review stays the substance
check. Blind substitution when fixing hits is itself a slop source: rewrite
the sentence, do not swap characters.

## Links

[[ADR-002-machine-gates]] [[ADR-009-devil-review]]
