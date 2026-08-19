---
type: adr
id: ADR-002
title: Machine gates with a single human point
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-002: Machine gates with a single human point

## Context

Committee-based validation recreates agile bureaucracy and dies under load.
Discipline-based validation fails silently (observed: stories reported "all
green" with no test backing, fixed only once a machine check was imposed).

## Decision

Creation plans pass a pipeline of executable gates (anti-dup, brief, schema,
testable, embodiment, slop, wiki), like a CI. Exactly one human point: the
gatekeeper, on the full path only. Fast path: green gates = activated.

## Consequences

No meetings; rejection messages are actionable; gate gaming remains possible
on pertinence, which is why the full path keeps its human and why traces are
judged after the fact.

## Links

[[ADR-003-ceremony-selector]] [[ADR-006-harness-enforcement]]
