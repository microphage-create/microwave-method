---
type: adr
id: ADR-010
title: Adopt-first, archive everything, migrate through the factory
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-010: Adopt-first, archive everything, migrate through the factory

## Context

No organization starts from zero: agents and prompts already sleep in
`.claude/` folders, repos, and note tools. A method that ignores the
existing estate ships a map with a hole exactly where the sprawl lives.

## Decision

Pass 0 (`flows/adopt.md`) scans the estate like an antivirus: one frozen
inventory entry per artifact found in `wiki/_archive/`, no judgment at scan
time, then a BACKLOG of dispositions (migrate / merge / keep-as-is /
retire) that the human prunes. Migrations run as ordinary pass-1 creations
seeded from their archive entry. Archive entries are exempt from card gates
and from the registry index (BACKLOG.md is their local index): the archive
is the one space where non-conforming artifacts are admitted, read-only.

## Consequences

The framework adapts to the estate instead of demanding a green field; even
with zero migrations, the adoption delivers a complete map of what exists.
Cost: the archive can be large; it is inert markdown and prunable by the
human.

## Links

[[ADR-001-two-pass-method]] [[ADR-005-two-plane-wiki]]
