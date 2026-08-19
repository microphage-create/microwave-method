---
type: adr
id: ADR-008
title: Bootstrapped light, self-hosting as soon as the factory runs
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-008: Bootstrapped light, self-hosting as soon as the factory runs

## Context

The framework is small by nature (a handful of templates, short stdlib
gates, one embodiment module): a full external method run (PRD, stories) would produce
artifacts nobody reads, failing our own consumption test on day one.

## Decision

Bootstrap with the lightest structure that compounds: a short brief and ADRs
written along the way (this wiki). The design document is the plan that
preceded the repo. As soon as the factory flow runs, Microwave creates its
own next module through itself (self-hosting), and external scaffolding
retires.

## Consequences

The repo is born with its memory (these ADRs). The first self-hosted creation
is the framework's own acceptance test.

## Links

[[ADR-001-two-pass-method]]
