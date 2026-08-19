---
type: learning
id: LRN-011
title: A heuristic that scans for verbs must understand negation
date: 2026-08-19
scope: microwave
---

# LRN-011: Heuristics must read negation

## What happened

The first real agent-card honestly documented itself as read-only:
"never writes", "Writes nothing". gate_schema's write-signal heuristic saw
"writes" and rejected the card, punishing the clearest possible read
declaration.

## Why (root cause)

The regex matched a write verb without reading the negation in front of or
behind it. Good documentation (stating what an agent does NOT do) tripped
the guard.

## How to apply

A word-level heuristic over prose must skip matches negated by never/no/
not/n't before, or "nothing" after. gate_schema now does. General rule:
any signal heuristic on human prose is wrong until it handles negation;
the devil and gatekeeper remain the real guard (the heuristic is a
tripwire, LRN-tripwire spirit).

## Links

[[ADR-003-ceremony-selector]] [[LRN-001-directories-lie]]
