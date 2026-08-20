---
type: adr
id: ADR-028
title: Agents are context or service, and the model carries the anti-sprawl
status: accepted
date: 2026-08-20
scope: meta
---

# ADR-028: Agents are context or service, and the model carries the anti-sprawl

## Context

"Anti-sprawl" rested on a cooperative convention (create only through the
factory) and a lexical anti-dup gate: a weak guarantee a reviewer sees through.
The real estates that work, like the author's own, already follow a shape:
**context** agents, one per repo, that carry that repo's conventions; and
**service** agents, transversal and reusable, that a context agent invokes
(copywriter, code-review). Naming that shape turns anti-sprawl from a promise
into a property.

## Decision

Every agent card declares `kind: context | service`.
- A **context** agent guards one repo: it must name it (`repo:`). One context
  per repo is a natural cardinality, so the registry does not fill with
  near-duplicates.
- A **service** agent is transversal and names no repo; it is shared, never
  copied.
- An agent may declare `uses: [service-slugs]`; `gate_uses` resolves each against
  the registry, spanning the federation ([[ADR-027-federated-index-crosses-the-repo-boundary]]),
  so a context in one repo can wire a service defined in another. Only `[service]`
  index lines satisfy `uses`.

The INDEX token carries the kind (`- [context] …` / `- [service] …`), so the
registry, which the runtime resolves through, states the taxonomy in one place.

## Consequences

Easier: anti-sprawl is now structural, not exhortation. One guard per room, shared
tools, and `uses` links that must resolve. The onboarding can scan a repo tree and
propose one context per repo plus the service catalog, because the model tells it
what to propose. Harder: existing single-kind thinking must be migrated (`kind` is
now required on every card), and agent-zero is filed as a `service` (the front door
is transversal), which is a slight stretch accepted for simplicity over a third
kind.

## Links

[[ADR-027-federated-index-crosses-the-repo-boundary]]
