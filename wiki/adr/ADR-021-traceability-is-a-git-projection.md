---
type: adr
id: ADR-021
title: Traceability is a projection over git, not a fourth registry
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-021: Traceability is a projection over git, not a fourth registry

## Context

"Delivery is the save" (ADR-019) raises a real need: in case of trouble, walk
from the broken code back to the reason for the code. Git already carries most
of it: `git blame` gives the SHA, `git show` the diff, the commit message the
short why. What git does NOT carry is the link from a commit to the ATOM that
holds the long why (the ADR or learning behind the decision). The tempting fix
is a fourth stored file linking SHA to atom. That is the exact trap ADR-020
forbids: the framework already has three overlapping index files (INDEX =
atoms, REGISTER = saves, LEDGER = governance events), and a fourth written in
parallel with git would desync the day a hook misses one. Two sources for one
truth is the rug.

## Decision

Traceability is a VIEW derived from git plus the atom files, generated on
demand, never a stored registry. `gates/trace.py` reads `git log`, and for
each commit extracts the atom ids named in its message, giving the commit-to-
atom projection both ways (a commit's atoms, an atom's commits). Single source
of truth stays git; nothing is written in double. The vocabulary is locked so
the three existing files stop colliding: INDEX indexes atoms, REGISTER indexes
saves, LEDGER logs governance events, trace PROJECTS git; none is "the
registry" alone.

The discipline that makes the link exist is one line, already practised: a
commit that lands an atom names that atom in its message. `trace.py --check`
is a manual check for ADR-020 orphans (run it yourself; it is wired into no
hook or CI yet) that flags any commit which ADDS an atom file without naming
it (a decision landing with no global trace). Scope
is deliberately tight so it never cries wolf: only ADDED atom files (a later
edit is covered by git blame, and a mass coherence pass touching many atoms
must not be punished), and only atom-bearing paths (`wiki/adr/`, project
learnings/bugs/features), never a docs or install commit.

## Consequences

In case of trouble: `git blame` to the SHA, `trace.py` (or the message) to the
atom, the atom to the full rationale. No fourth file to keep in sync. Follow-up
(specified, not yet shipped, like gate_design/gate_code in ADR-016): wire
`trace.py --check` into a commit-msg hook so the miss is caught at commit time,
not only in CI. History predating this rule carries orphans; they are reported,
not rewritten, and the rule holds going forward.

## Links

[[ADR-020-verify-global-impact]] [[ADR-019-capture-triggers-on-context-pressure]] [[ADR-014-continuous-measurement]] [[ADR-005-two-plane-wiki]]
