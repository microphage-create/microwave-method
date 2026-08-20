---
type: adr
id: ADR-027
title: A federated index carries anti-dup across the repo boundary
status: accepted
date: 2026-08-20
scope: meta
---

# ADR-027: A federated index carries anti-dup across the repo boundary

## Context

The pitch is "one central inventory nobody can escape". The registry, though,
lives in a repo, so `gate_antidup` only ever saw the repo it ran in. An
enterprise runs many repos: two teams in two repos could create the same agent
and no gate would catch it. The agent itself was never the problem, a
contextualizing agent already spans repos, but the anti-dup surface stopped at
the repo wall, and a reader who clones the code sees that gap immediately.

## Decision

Ship `gates/federated_index.py`. A repo declares a federation in
`.microwave/federation` (one sibling repo path per line). `gate_antidup` then
compares a new card against the local registry AND every federated one at once,
and a hit names the repo that already holds the overlapping agent. Only each
repo's `wiki/INDEX.md` is read, so it stays cheap and stdlib-only ([[ADR-007-stdlib-gates]]).
A listed repo that is absent or has no registry is skipped in silence: a
federation must never turn a teammate's missing checkout into a red CI. No
manifest means no federation, and the anti-dup surface is byte-for-byte the
former local-only one, so the single-repo default is untouched.

## Consequences

Easier: the "central inventory" claim now holds past one repo, and
`python gates/federated_index.py` prints the cross-repo agent map an org actually
wants. Harder: the manifest is a per-repo declaration a human maintains, and it
federates by reading sibling checkouts, not a live service, so a repo the machine
cannot reach is simply out of view rather than blocking. That is the deliberate
trade: degrade to local, never fail the federation.

## Links

[[ADR-007-stdlib-gates]]
