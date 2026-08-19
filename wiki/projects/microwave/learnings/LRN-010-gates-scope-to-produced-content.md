---
type: learning
id: LRN-010
title: A gate installed on a host repo governs only what it produces, not the host's files
date: 2026-08-19
scope: microwave
---

# LRN-010: Gates scope to produced content, not the host

## What happened

Installing Microwave onto a real repo, gate_slop swept the host's own
CLAUDE.md and flagged its em dashes. The gate was about to reject files
the framework did not produce and has no business policing.

## Why (root cause)

gate_slop scanned root docs, flows/, and wiki/, which on the framework's
own repo means its docs, but on a host repo means the host's unrelated
files. A gate that punishes pre-existing host content cannot be installed
anywhere.

## How to apply

A gate governs only the content the agents PRODUCE: `wiki/` atoms.
gate_slop now scans wiki/ only (single files can still be checked on
demand). The host's own files are never policed by an installed gate.
General rule for any future gate: default its scope to wiki/, never the
host repo.

## Links

[[ADR-011-anti-slop]] [[ADR-010-adopt-first]]
