---
type: adr
id: ADR-019
title: Delivery is the save; context pressure is only a residue net
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-019: Delivery is the save; context pressure is only a residue net

## Context

LRN-006 was right that capture must ride the critical path and never depend
on the user's judgment (a discretionary capture dies). But it assumed the
end-of-session save WAS that path. It is not: "session end" has no reliable
signal. The terminal can be closed abruptly, no event fires, and at the
moment a session-end hook would run there is no longer an agent to write an
intelligent synthesis. Worse, the fear it addresses is misdiagnosed. Two
losses were conflated: raw data (every keystroke) and reusable synthesis
(where I was, which decisions). The raw transcript is already written
continuously by the harness, so the bytes are never lost. What dies at
compaction or on an abrupt close is the synthesis, and only that.

## Decision

- Delivery IS the save. The moment work is built or shipped it is already
  consigned: the commit is the save, the git log is the journal, an atom
  written or a deliverable committed sits on disk the instant it exists.
  Produced work is never "to save later"; producing it saves it. Everything
  below covers ONLY what delivery does not: reasoning not yet materialized,
  and the resume point of unfinished work. Both are small, and shrink to
  nothing the more one commits per delivery.
- The raw transcript covers data loss. A condensed save protects the
  reusable synthesis, not the bytes. We never sell "it saves everything";
  it saves what will be reread.
- Consumable atoms are traced AT RESOLUTION, not held for session end: the
  instant a unit of work resolves into something a consumption test passes
  (a decision, a learning, an agent card), the agent writes its atom then
  and there, without asking. The two deployment learnings of this session
  were traced this way, unprompted, the second a gate was fixed.
- As a FALLBACK for that residue, never the mechanism, the condensed session
  save is PROPOSED on an objective trigger, never on
  mood and never on the undetectable "session end": context pressure (the
  window running high, before compaction overwrites the detail) AND unlogged
  consumable work since the last save. Both conditions, or silence. One
  nudge per threshold crossing. High threshold makes it rare; the second
  condition makes it relevant; together they answer the only real dilemma
  (nagging vs losing work).
- Three tiers catch each other, none sufficient alone: the agent traces or
  proposes at resolution (semantic judgment, the strongest signal); the user
  may run `save` by hand anytime (voluntary fallback); the pre-commit hook
  flags the mechanical miss at commit time (cards or atoms changed but the
  ledger or register did not). The agent judges WHAT is worth keeping; the
  hook only catches a measurable omission.
- The trigger reserves headroom. "Context pressure" means the compaction
  threshold MINUS the token cost of a save, never "context full". A save
  spends tokens (writing atoms and the summary, running the gates); fire it
  too late and compaction hits mid-save, failing exactly when it matters.
  Two corollaries: tracing at resolution keeps the final save cheap (little
  left to write), and the save writes most-recoverable-first (id, register
  line, next-steps skeleton, committed early, then enriched), so even an
  interrupted save leaves a resume point.
- Session end becomes a voluntary net, not the mechanism.

This refines LRN-006, it does not overturn it: judgment still leaves the
user (it moves to the agent and to an objective trigger), and capture still
rides the critical path. The correction is only WHICH path is reliable: the
commit and the context threshold, not the phantom "session end".

## Consequences

Capture no longer waits on an event that may never fire. The pre-commit
hook gains a check (cards/atoms changed without a matching ledger/register
line: warn), specified here, not yet shipped, like gate_design/gate_code.
`flows/save.md` documents the trigger so a future agent knows when to
propose. The honest limit stands: the agent tracing at resolution depends on
the agent's discipline; that is why the mechanical hook and the voluntary
`save` sit under it.

## Links

[[ADR-012-session-saves]] [[ADR-014-continuous-measurement]] [[LRN-006-capture-on-the-critical-path]]
