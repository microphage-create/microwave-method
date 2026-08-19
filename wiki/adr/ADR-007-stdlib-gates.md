---
type: adr
id: ADR-007
title: Gates are Python stdlib only, parsing a defined YAML subset
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-007: Gates are Python stdlib only, parsing a defined YAML subset

## Context

The gates must run anywhere a coding agent runs: pre-commit, CI, bare
laptops. Every dependency is an installation failure mode and an adoption
tax.

## Decision

All gates use the Python 3.10+ standard library only. Frontmatter is YAML
restricted to a defined subset (scalar `key: value`, nested maps at 2-space
indentation, `- ` item lists, inline `[a, b]` lists, quoted or bare strings),
parsed by `gates/_lib.py`. Templates are the contract: if the template
validates, any conforming card validates.

## Consequences

Zero-install gates; the YAML subset is a documented constraint of the card
format, checked by `gate_schema`. Anything fancier than the subset belongs in
the markdown body, not the frontmatter.

## Links

[[ADR-002-machine-gates]]
