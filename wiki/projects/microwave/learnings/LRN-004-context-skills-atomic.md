---
type: learning
id: LRN-004
title: Repo-bound context agents are atomic, never merge across contexts
date: 2026-08-19
scope: microwave
---

# LRN-004: Repo-bound context agents are atomic

## What happened

During the first REX, the machine-proposed deep cut suggested merging two
context agents bound to different repos. The gatekeeper struck it down:
each context agent loads one world (one repo, one mission, its secrets,
its conventions); merging two would build an agent that loads foreign
context by design.

## Why (root cause)

Consolidation pressure treats every pair of similar-looking agents as
merge candidates. Context loaders LOOK similar (same shape: load brief,
load repo, work) while being maximally different in content.

## How to apply

The MISSION is the atomic context boundary; the repo is its default
indicator, not the rule itself. Refined by a second gatekeeper ruling:
two repos coupled as source-of-truth and its renderer (a wiki and the
site that consumes it) are ONE mission and may merge. Two unrelated
missions never merge, one repo each or not. Applied to `flows/adopt.md`
(merge disposition) and `flows/devil-review.md` (duplication surface).

## Links

[[ADR-010-adopt-first]] [[ADR-005-two-plane-wiki]]
