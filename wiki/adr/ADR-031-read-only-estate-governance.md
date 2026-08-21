---
type: adr
id: ADR-031
title: Estate-level governance is read-only, it names but never moves
status: accepted
date: 2026-08-21
scope: meta
author: estate-guard + @microphage-create
---

# ADR-031: Estate-level governance is read-only, it names but never moves

## Context

An estate guardian that maps a folder of repos and proposes a cleaner layout is
one autocorrect away from a footgun: a wrong consolidation, a mis-judged archive,
a rename that breaks a path is data loss, and trust in an automated tidier
collapses on its first bad move. The whole value of the guardian is that a human
can run it on thirty folders without fear. That only holds if it cannot act.
Marcel set the constraint in his own words: "sans jamais toucher le code", just
tidy and advise, never act.

## Decision

Estate-level governance (the `estate-guard` agent, `gates/estate_hygiene.py`) is
read-only. It declares arbitrary house rules and emits a verdict per repo (rename
to X, file under Y, or OK), then prints the target tree. It never moves, renames,
writes, or deletes. The human applies the verdicts by hand. This is the estate
counterpart to a context agent: repo-guard checks one repo from the inside, the
guardian imposes conventions across the folder from the outside, and neither
mutates.

## Consequences

Easier: the guardian is safe to run anytime, needs no undo, and stays trustworthy
because it cannot cause the loss it warns about. Harder: the human does the
mechanical moves the guardian only names. Forbidden: any filesystem-mutating call
in the tool. The ban is guarded, not merely asserted, by a tree-snapshot test
(`test_report_never_mutates_the_estate`, which fails if any path changes) and a
card grep against write and move primitives (a guard against a mutation creeping
in, not an absolute proof: a shell-out could still write).

## Links

[[estate-guard]] [[ADR-007-stdlib-gates]] [[ADR-021-traceability-is-a-git-projection]]
