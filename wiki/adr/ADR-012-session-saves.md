---
type: adr
id: ADR-012
title: Atomic session saves with a registered, resumable id
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-012: Atomic session saves with a registered, resumable id

## Context

Sessions end; context dies with them. Proven in months of daily operation
by the author's private system: an end-of-session save with a strict format
(task in progress, done, decisions, files, next steps) makes any session
resumable by a cold agent. The framework had the wiki but not the ritual
that feeds it, and single-file notes miss the point: a session produces a
BATCH (save + untraced atoms + register lines) that must land coherently.

## Decision

`flows/save.md` writes the batch atomically: session save
(`templates/session-save.md`, id `S-YYYYMMDD-NN-slug`), the session's
untraced atoms, the register line in `wiki/sessions/REGISTER.md`, then the
gates validate the whole batch BEFORE the register line counts, and one
commit persists it. `flows/resume.md` recovers any save from its id, from
any machine holding the repo: the register is the lookup table, git is the
transport, versioning stays git's job (a save is a semantic resume point,
not a diff). Saves are append-only history and are exempt from the main
INDEX: REGISTER.md is their local index (ADR-010 pattern).

## Consequences

Any session is recoverable by dictating one id. Untraced work becomes
visible at save time ("Atoms produced: none, because..."), which is where
compounding is won or lost. Cost: a real end-of-session ritual; kept cheap
by the template.

## Links

[[ADR-005-two-plane-wiki]] [[ADR-010-adopt-first]]
