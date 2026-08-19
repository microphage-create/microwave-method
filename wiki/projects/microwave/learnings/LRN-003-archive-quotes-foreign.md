---
type: learning
id: LRN-003
title: Inventory entries quote foreign content, exempt the archive from link checks
date: 2026-08-19
scope: microwave
---

# LRN-003: The archive quotes a foreign estate

## What happened

An inventory entry quoted a wikilink token verbatim from the scanned
estate; gate_wiki flagged it as a broken link of OUR wiki and blocked the
batch. Same class of finding: a scan surfaced an inline confidential
section in a client-facing artifact, proving the scan doubles as a leak
audit.

## Why (root cause)

Archive entries record what IS, including syntax that collides with the
governed wiki's own conventions.

## How to apply

gate_wiki now exempts wiki/_archive/ from wikilink resolution (fixed).
Adopt scans should also flag confidentiality leaks found in the estate as
fix-first backlog items: added to the practice.

## Links

[[ADR-010-adopt-first]] [[ADR-011-anti-slop]]
