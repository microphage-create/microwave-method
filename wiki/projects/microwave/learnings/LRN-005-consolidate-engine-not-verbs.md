---
type: learning
id: LRN-005
title: Consolidate the engine, never the frequent entry points
date: 2026-08-19
scope: microwave
---

# LRN-005: Consolidate the engine, not the frequent verbs

## What happened

The machine proposed merging four session-lifecycle agents into one hub
with modes. The gatekeeper rejected it on usage grounds: a hub-with-modes
turns the daily reflex `/save` into `/session save`, adding friction to
the most frequent gesture. The consolidation would have cost more than it
saved.

## Why (root cause)

Sprawl-reduction pressure counts objects (fewer agents = better) and
ignores ergonomics. But a frequent verb is a first-class shortcut, not an
implementation detail; collapsing it under a mode selector is a
regression measured in keystrokes-per-day.

## How to apply

Merge the ENGINE (shared logic, one registry, bugs fixed once), keep the
VERBS (short direct entry points for frequent actions). A "hub" is a
shared backend with several doors, never one door with modes. Applied to
`flows/adopt.md` merge disposition and the merge rule: a merge is legal
only if it does not lengthen a frequent gesture. Rare or one-off verbs
collapse into a smart DEFAULT rather than a mode: bare `resume` jumps to
the most recent active save of the current scope, no id typed; daily verbs
stay top-level. Frequency decides ergonomics.

## Links

[[ADR-012-session-saves]] [[LRN-004-context-skills-atomic]]
