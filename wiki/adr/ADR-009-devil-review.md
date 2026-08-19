---
type: adr
id: ADR-009
title: Fresh-eyes devil review before full-path judgment
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-009: Fresh-eyes devil review before full-path judgment

## Context

Machine gates verify form, not substance: criteria gaming, real duplication
of purpose, and dishonest blast radius all pass mechanical checks. The
creator cannot be their own red team, and the human gatekeeper should not be
the first substantive reader.

## Decision

Full-path creations pass an adversarial review by a FRESH agent session (no
creation context, no memory across rounds) following `flows/devil-review.md`.
The creator fixes all objections and requests a new fresh devil until one
returns zero objections. The gatekeeper judges only cards with a
zero-objection devil report attached.

## Consequences

Substance is attacked by a neutral reader before human time is spent; the
devil clears form and intent, the gatekeeper keeps the opportunity judgment.
Cost: one or more extra agent sessions per full-path creation, accepted
because full-path agents are the dangerous ones.

## Links

[[ADR-002-machine-gates]] [[ADR-003-ceremony-selector]]
