# Flow: adopt (Pass 0: scan the existing estate)

Microwave is rarely installed on a green field. Before anything is created,
the existing estate is scanned like an antivirus scans a disk: everything
found is archived, nothing is judged yet, and the archive becomes the
shopping list of what to migrate.

## Before you scan: never archive a secret

The archive is committed to git, so the scan must not capture a secret. Exclude
credential-bearing paths outright: `.env`, `.env.*`, `**/secrets/**`, `*.pem`,
`*.key`, `id_rsa` / `id_*`, and anything under `.git/`. Record METADATA about
each artifact (provenance, apparent mission, apparent blast radius), never its
raw file body: if a location is a whole repo, read it, do not copy its contents
into the archive. When in doubt, skip it and note the skip, do not archive it.
Tell the human, before scanning, that the archive will be committed.

## Step 1: Point at the estate

Ask the human where their agents sleep. Typical answers: a `.claude/`
directory (commands, agents, skills), a `prompts/` folder, a GitHub repo, a
Notion export, scattered `*.md` system prompts. Take ALL locations given.

## Step 2: Scan and archive (one entry per artifact, no judgment)

Walk every location. For EVERY artifact found, write one
`templates/inventory-entry.md` into `wiki/_archive/`. Record what IS, not
what should be: provenance, apparent mission, apparent blast radius,
last-touched date, references. CLASSIFY ITS FORM (ADR-015): is it an
**agent** (acts, has a blast radius), a **data-source** (a wiki/KB/index
read by agents), a **tool** (a function agents call), or a **doctrine**
(rules/context injected)? Do not default everything to "agent": a wiki
filed as a skill is a data-source. Do not fix, do not skip "obviously dead" ones: dead entries are
findings too (they document the sprawl you are adopting your way out of).

The archive is the only space where non-conforming artifacts are admitted:
frozen, read-only, listed.

## Step 3: The shopping list

Compile `wiki/_archive/BACKLOG.md`: every entry, one line, with a proposed
disposition and a priority:

- `migrate`: recreate through the factory (`flows/create-agent.md`); the
  archived entry becomes the elicitation input of pass 1, which makes
  migrations the cheapest creations.
- `merge`: an existing or planned agent absorbs it (name which). Merge
  rule: the MISSION is the atomic boundary (the repo is its usual
  indicator). Merge siblings of the same mission, generic tool agents, or
  a source-of-truth and its SINGLE consumer. Never two unrelated
  missions. And never at the cost of a frequent gesture: merge the ENGINE
  (shared logic, one registry), keep the short VERBS as direct entry
  points (LRN-005). A hub is a shared backend with several doors, not one
  door with modes. A source of truth read by MANY consumers is never
  merged into one of them: it stays a shared layer they all read
  (LRN-007).
- `keep-as-is`: runs outside Microwave for now, listed so it is never
  invisible again.
- `reshape`: the artifact is in the wrong form (ADR-015); move it to the
  right one (a wiki masquerading as a skill becomes a data-source in the
  wiki layer; a function dressed as an agent becomes a tool). Dispositions
  below apply per form: only agents migrate/merge.
- `retire`: propose for deletion; a human confirms.

Sort by: agents people actually use first, dead weight last. The human
prunes and reorders: the backlog is a proposal, not a verdict.

## Step 4: Migrate at your own pace

Each `migrate` line is executed as a normal pass-1 creation, seeded from its
archive entry. Tick lines off in the BACKLOG as dispositions complete. The
adoption is finished when the backlog holds no unprocessed `migrate` or
`merge` lines: `keep-as-is` may legitimately live forever.

## Why this phase exists

The framework adapts to the estate, not the reverse. And even when nothing
is migrated yet, the archive already delivers the first promise of the
method: a complete, honest map of what exists, which nobody had.
