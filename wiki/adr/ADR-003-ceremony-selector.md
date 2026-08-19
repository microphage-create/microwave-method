---
type: adr
id: ADR-003
title: Ceremony proportional to blast radius
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-003: Ceremony proportional to blast radius

## Context

Fixed-depth methods are either too long for trivial agents or too shallow for
dangerous ones. "Light but structured" must be a computed property, not a
slogan.

## Decision

The card's `blast_radius` (`read` | `write` | `spend` | `prod`) selects the
path. `read` → fast path (minutes, no human). Anything that writes, spends or
touches production → full path (full elicitation, deep anti-dup, gatekeeper
before activation). The selector is the agent's power, never the creator's
mood.

## Consequences

Trivial agents cost minutes; powerful agents cannot skip judgment. The
selector itself is validated by `gate_schema` (enum) and misdeclaring blast
radius is an auditable offense visible in the card's interfaces.

## Links

[[ADR-001-two-pass-method]] [[ADR-002-machine-gates]]

## Amendment (2026-08-19): the fast path is 3 steps or it failed

The fast path (read-only) is spec, gate, activate: three visible steps,
embodiment optional. If it grows past three, ceremony has crept back in
(the anti-gas-factory tripwire). Guards (elicit, embody, build, devil,
gatekeeper, seed) attach only on the full path, only when the agent can do
damage.
