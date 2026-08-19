---
type: learning
id: LRN-008
title: Classify an artifact's form before deciding its fate
date: 2026-08-19
scope: microwave
---

# LRN-008: Classify form before disposition

## What happened

I proposed merging a personal wiki with the site that reads it, having scanned it as a "skill" like the other 66. It is not a skill:
it is a data source read by several agents. The merge would have been a
category error with real data loss. I reasoned "what to merge" instead of
"what form should each thing be".

## Why (root cause)

The adopt scan tagged every artifact `kind: skill`. With one label, every
difference of FORM (agent vs data vs tool vs doctrine) was invisible, so
consolidation treated a database like an agent.

## How to apply

Classify form FIRST (agent / data-source / tool / doctrine, ADR-015),
then decide disposition. A data-source read by many is never an agent to
merge; it is a shared layer to keep (LRN-007). The right question is not
"which agents merge" but "is each thing in the form that serves it best,
and how is it best consumed".

## Links

[[ADR-015-artifacts-have-a-form]] [[LRN-007-shared-source-stays-a-layer]]
