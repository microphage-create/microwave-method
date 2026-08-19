---
type: adr
id: ADR-004
title: Embodiment for powerful agents, optional for read-only
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-004: Embodiment for powerful agents, optional for read-only

## Context

Adoption is the documented graveyard of knowledge systems (catalogs unused,
lessons-learned unknown to their audience). An agent invoked by a memorized
command dies; practitioner demand for per-agent terminal identity is public
and unserved.

## Decision

Pass 1 includes a mandatory embodiment step: icon, short name, themed terminal
profile, launcher. Terminals dressed as apps, not apps replacing the terminal.
One identity manifest in the card; one adapter per OS (Windows Terminal,
iTerm2/Terminal.app, freedesktop). `gate_embodiment` blocks activation
without a body. The human validates the icon.

## Consequences

Every agent is visible, launchable, and identifiable at a glance in parallel
sessions. Adapters must back up configs, stay additive, and know how to
uninstall what they added.

## Links

[[ADR-001-two-pass-method]]

## Amendment (2026-08-19)

Embodiment is mandatory only for agents that can do damage (write/spend/
prod), so they are recognizable among live sessions. A read-only,
throwaway agent may activate bodiless, with no embodiment block at all
(anti-ceremony, [[ADR-003-ceremony-selector]]). `gate_schema` and
`gate_embodiment` require the manifest only for powerful agents.
