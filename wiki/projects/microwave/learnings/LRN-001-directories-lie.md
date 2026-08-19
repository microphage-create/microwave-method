---
type: learning
id: LRN-001
title: Manual directories lie by omission, scan files not indexes
date: 2026-08-19
scope: microwave
---

# LRN-001: Manual directories lie by omission

## What happened

First real adopt run (67-skill estate): 11 of 67 skills existed in no
manual directory at all, including two the estate's own doctrine cites as
mandatory. The directories were maintained by convention for months.

## Why (root cause)

A hand-maintained index has no enforcement loop: nothing fails when a file
is born outside it.

## How to apply

The adopt scan must walk the FILES and cross-check the indexes, never
trust them. This is also the core sales argument for a runtime-consumed
registry guarded by gate_wiki.

## Links

[[ADR-010-adopt-first]]
