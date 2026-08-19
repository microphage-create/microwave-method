---
type: learning
id: LRN-007
title: A source of truth with many consumers stays a shared layer, never merged into one
date: 2026-08-19
scope: microwave
---

# LRN-007: A shared source of truth stays a layer

## What happened

LRN-004 said "repos coupled as source-of-truth and renderer are one
mission and may merge". The gatekeeper found the hole: a personal wiki
feeds not one site but several consumers (the site, the career module, the
CV). Merging the wiki into the site would cut the career module off from
it. Contexts form a graph, not a clean partition.

## Why (root cause)

The merge heuristic assumed one-to-one coupling. Real estates have
one-to-many: a data source read by multiple missions. Absorbing it into
one consumer breaks the others silently.

## How to apply

Count the consumers. A source of truth with ONE consumer may merge with
it. A source of truth with MANY consumers stays SEPARATE as a shared
layer that all of them read; it is never absorbed into any single
consumer. This is exactly the two-plane wiki and the index-first registry
(ADR-005): shared context is a layer, not a sibling. Refines LRN-004's
merge rule; applied to `flows/adopt.md` and `flows/devil-review.md`.

## Links

[[ADR-005-two-plane-wiki]] [[LRN-004-context-skills-atomic]]
