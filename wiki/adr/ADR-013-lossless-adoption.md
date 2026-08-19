---
type: adr
id: ADR-013
title: Adoption is lossless, conversion wraps and never rewrites
status: distilled
date: 2026-08-19
scope: meta
---

# ADR-013: Adoption is lossless, conversion wraps and never rewrites

## Context

Real estates carry years of accumulated knowledge in formats the framework
does not prescribe (the first REX estate: 192 session notes, 147 memory
files). The owner's constraint is absolute: improve the existing system
without destroying anything, never lose data. A migration that rewrites
content into a new shape silently loses whatever the shape did not expect.

## Decision

Four rules, in order, all mandatory:

1. **Copy first.** Before any conversion touches an estate, a dated backup
   of the affected data is written outside the working tree. No backup, no
   conversion.
2. **Wrap, never rewrite.** Converting a legacy artifact means adding
   frontmatter (id, type, provenance) AROUND the original body. The body
   stays byte-identical; original frontmatter keys are preserved alongside
   the new ones (extra keys are legal by contract).
3. **Originals stay.** The source file remains in place (or in the
   archive) as the provenance trace, referenced by `converted_from:`.
   Deletion of originals is a separate, human-confirmed act, never part of
   conversion.
4. **Unconvertible data stays readable.** Whatever fits no template lands
   in the archive as-is, listed, never dropped.

Verification: a conversion run must prove body integrity (hash of the body
before and after) and pass the gates before its register lines count.

## Consequences

Migrations become reversible by construction and auditable by diff. Cost:
converted files carry legacy keys and occasional legacy formatting; that
is the price of zero loss, and gate_slop exempts nothing retroactively
(legacy bodies are quoted history, scanned but fixable lazily).

## Links

[[ADR-010-adopt-first]] [[ADR-012-session-saves]]
