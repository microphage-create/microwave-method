---
type: improvement-report
id: IR-002
title: sync overwrites the install work-tree with no reviewable or revertable unit
kind: idea
surface: other
severity: slows
status: shipped
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

Two options were on the table: a dedicated integration branch per sync, or a
plain changed-paths manifest. Chosen: **make the sync a commit**, which beats
both. A commit is at once the reviewable unit (`git show`) and the revertable
one (`git revert`) — the manifest gives only the first — while committing on the
current branch avoids the branch-switching ceremony that made the integration
branch heavy. An opt-in `--commit` runs the sync, gate-checks the estate, and on
green commits ONLY the framework files it changed (pathspec-limited), so the
operator's estate edits stay uncommitted. Default behavior is unchanged.

## Ship

Shipped install-side: `dev-loop/sync.py` is install-local plumbing (in
`ESTATE_PRESERVED`, never synced from source), so the fix lives in the install,
not this repo. Commit `5f5c4e8` on the install adds `--commit`. Verified: an
isolated git test proves the sync commit excludes an uncommitted estate edit;
a real 0-change `--commit` on the install runs the gates and makes no spurious
commit. This report is closed here for the idea-box record.
