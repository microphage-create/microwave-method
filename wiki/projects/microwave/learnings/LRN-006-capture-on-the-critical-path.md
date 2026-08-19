---
type: learning
id: LRN-006
title: Capture belongs on a ritual moment, never to discretionary initiative
date: 2026-08-19
scope: microwave
---

# LRN-006: Capture belongs on the critical path

## What happened

The migration retired a standalone quick-capture agent: in practice
nobody ever triggered it. The blocker was not friction of typing, it was
friction of JUDGMENT: it asked the user to decide, mid-flow, whether a
thought was worth capturing. That decision never gets made.

## Why (root cause)

A capture gesture that depends on discretionary initiative sits off the
critical path and dies (the manifesto's own lesson: NASA's LLIS, unused
because it was optional). The end-of-session save sits ON the critical
path: it is a mandatory ritual moment, so it captures everything without
asking the user to judge.

## How to apply

Do not ship discretionary capture agents. Bind capture to a ritual the
user already performs (session end via `flows/save.md`), where the flow
does the judging ("Atoms produced: none, because..."). One less agent,
better capture. Applied to the adopt retire heuristic: a capture agent
with no ritual anchor is a retire candidate by default.

## Links

[[ADR-012-session-saves]] [[LRN-005-consolidate-engine-not-verbs]]
