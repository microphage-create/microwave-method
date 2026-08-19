---
type: adr
id: ADR-006
title: Harness-level enforcement; constitution, not dogma
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-006: Harness-level enforcement; constitution, not dogma

## Context

Rules that live in prompts or wikis are followed until pressure. The proven
pattern is the permission deny-rule: the harness refuses, goodwill is not
involved.

## Decision

Rules are enforced structurally at three floors, shipped as installable
artifacts: permission deny-rules (agents cannot read secrets, write main wiki
spaces directly, or modify gates), blocking hooks (out-of-band creation
refused at execution), repo protection (required checks + CODEOWNERS on
`gates/`: humans cannot merge red). Rules are inviolable in execution and
amendable ONLY through `flows/amend-rule.md`. Emergencies use a traced
break-glass with mandatory post-mortem.

## Consequences

The system survives its operators' bad days. A rule frozen with no amendment
path would push users to desert the system; the amendment flow prevents that
while keeping zero bypass.

## Links

[[ADR-002-machine-gates]]
