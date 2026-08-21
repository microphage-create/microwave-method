---
type: improvement-report
id: IR-002
title: sync overwrites the install work-tree with no reviewable or revertable unit
kind: idea
surface: other
severity: slows
status: open
scrubbed: true
date: 2026-08-21
source_signal: dogfood
---

# IR-002: sync overwrites the install work-tree with no reviewable or revertable unit

## The shape

`dev-loop/sync.py` copies each framework file straight into the install's
work-tree with `shutil.copy2`, file by file. After a sync the operator sees a
pile of modified files but no single object that says "this is what this sync
changed" and no clean way to undo just that sync. The `--check` guard runs the
install's gates after the copy, so a sync that breaks the estate is caught, but
a sync that passes the gates yet is unwanted still has to be untangled by hand
from the work-tree. There is no atomic, reviewable, revertable sync unit.

## Reproduce

1. Run `python dev-loop/sync.py` (or `--check`) against an install.
2. Framework files are overwritten in place in the work-tree.
3. Ask "what did this one sync change, and how do I revert exactly it?" There
   is no changeset object to answer with: only the raw work-tree diff, mixed
   with whatever else is uncommitted.

## Fix or idea

Give each sync a reviewable, revertable unit. Options, cheapest first:
land the sync on a dedicated integration branch (one commit per sync, so the
diff and the revert are a single git object); or have `--check` emit a summary
manifest of the paths it changed. Open question: branch-per-sync adds git
ceremony to a loop meant to be fast, so weigh it against a plain manifest
before building. Design needed before code; this stays an idea, not a queued
fix.

## Ship

Not shipped. Open idea, pending a design decision (integration branch vs
manifest). No branch yet.
