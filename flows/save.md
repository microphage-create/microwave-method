# Flow: save (atomic session checkpoint)

End-of-session ritual. It writes ONE coherent batch: the session save, the
atoms the session produced but never traced, and the registers. A save that
does not pass the gates does not enter the register: atomicity is enforced
by validation, versioning is git's job (the save is the semantic resume
point, not a diff).

## When this fires

Delivery is the real save: a commit consigns what it ships, so produced work
never waits on this flow. This flow is the FALLBACK for what delivery leaves
behind, the resume point of unfinished work. It fires not at "session end"
(no reliable signal, agent gone) but when the context window runs high AND
consumable work is unlogged since the last save, one nudge per threshold,
reserving headroom for the save's own token cost. You may also run it by
hand anytime. The raw transcript already holds the bytes; this holds the
reusable synthesis (ADR-019).

## Step 1: Allocate the id

Read `wiki/sessions/REGISTER.md`. The id is `S-<YYYYMMDD>-<NN>-<slug>`:
today's date, the next two-digit sequence for today, a short kebab slug of
the session subject.

## Step 2: Write the batch

1. Fill `templates/session-save.md` into `wiki/sessions/<id>.md`. Scan the
   whole session honestly: task in progress, done, decisions, files, next
   steps.
2. Trace the untraced: any decision, learning, or bug from this session
   that deserves an atom and has none gets one NOW
   (`templates/adr.md` / `learning.md` / `bug.md` into the project wiki,
   plus their `wiki/INDEX.md` lines). Link them in "Atoms produced".
3. Append the register line to `wiki/sessions/REGISTER.md`:
   `- S-... | YYYY-MM-DD | agent | scope | one-line summary`
4. Append the session's governance events to `wiki/metrics/LEDGER.md`
   (agents created, defects intercepted, purges): the ledger is only as
   true as the flows that feed it (ADR-014, `flows/metrics.md`).

## Step 3: Validate the batch

```
python gates/gate_wiki.py
python gates/gate_slop.py
```

Red gates: fix the batch, re-run. The register line stays only when green.

## Step 4: Persist

Commit the batch as one commit (`save: <id>`), push if a remote exists.
That is what makes the id recoverable from any machine and any session:
the wiki travels with the repo, the register is the lookup table.

## Closing a save

When the work a save points to is finished, flip its `status:` to `done`
in the save file (the register line stays: history is append-only).
