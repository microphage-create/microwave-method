---
type: adr
id: ADR-026
title: Decay gives the wiki an end-of-life, so it does not only grow
status: accepted
date: 2026-08-20
scope: meta
---

# ADR-026: Decay gives the wiki an end-of-life, so it does not only grow

## Context

A wiki that only grows becomes a graveyard: after months, hundreds of atoms, and
nobody can say which are still true. "A lifecycle that retires the dead" was a
claim in the pitch with no mechanism behind it, which a reviewer who reads the
code will notice.

## Decision

Ship `gates/decay.py`. An atom is a candidate for archival only if it is BOTH
orphan (no other atom wikilinks to it, so nothing reheats it) AND old (its last
git commit is older than
`--days`, default 90). It reports candidates, never deletes: humans delete
(ADR-020). It runs on demand or in a scheduled job, not in the pre-commit hook,
like `metrics.py` and `trace.py`.

## Consequences

Easier: the wiki has a real end-of-life; "retires the dead" is now executable, not
rhetoric. Harder: nothing is automatic, a human still moves candidates into
`wiki/_archive/`. The two-signal rule (orphan AND old) is deliberately
conservative, to avoid reaping a referenced-but-old atom or a fresh orphan.

## Links

[[ADR-020-verify-global-impact]]
