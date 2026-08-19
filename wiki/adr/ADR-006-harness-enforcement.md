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

Enforcement is split honestly (docs/governance.md). STRUCTURAL, a machine
refuses: the pre-commit hook and CI run the gates and block a red commit, and
CODEOWNERS plus branch protection gate the protected space (`gates/`, `flows/`,
`hooks/`, `harness/`, CI, `CODEOWNERS`, `wiki/adr/`) so no one merges red once
branch protection is on. COOPERATIVE, the agent or harness must play along: the shipped
permission deny-rules (`harness/`) cover the Read and Write TOOLS only, not the
shell, so they are a hint, not a sandbox and not secret protection; the flows and
the gatekeeper's judgment are convention. Rules are amendable only through
`flows/amend-rule.md`; emergencies use a traced break-glass with a post-mortem.

## Consequences

The fence that actually holds is the commit boundary (CI plus branch
protection); everything above it is discipline the flows encourage, stated as
such rather than claimed as a guarantee. A rule frozen with no amendment path
would push users to desert the system; the amendment flow prevents that.

## Links

[[ADR-002-machine-gates]]
