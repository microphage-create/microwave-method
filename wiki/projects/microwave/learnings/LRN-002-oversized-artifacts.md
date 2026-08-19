---
type: learning
id: LRN-002
title: Oversized artifacts break scans, flag them instead of choking
date: 2026-08-19
scope: microwave
---

# LRN-002: Oversized artifacts break scans

## What happened

One artifact of the scanned estate was 1905 lines, beyond the scanner's
comfortable read window; the agent had to fall back to partial reads plus
heading scans and said so.

## Why (root cause)

Estates accumulate monster files precisely because nothing measures them.

## How to apply

The adopt flow should treat oversized artifacts as findings: record
"oversized, partial scan" in the inventory entry and propose a split in
Notes for migration. Honesty about partial coverage beats fake
completeness.

## Links

[[ADR-010-adopt-first]]
