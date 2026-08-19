# Rules

The live, compact rule base: one actionable line per rule. This is what a
human or an agent reads, not the ADRs. ADRs are archived rationale (the
why), opened on demand; enforcement lives in the code (the gates). A
decision, once applied and distilled here, stops being a document to read.
Doctrine distills, it does not accumulate (the anti-gas-factory rule).

## Method

- One recursive method, two passes: pass 1 heavy once per agent, pass 2
  light per feature (intent + a short story with executable done-criteria,
  no PRD; the card and wiki are the context; trace to the wiki).
- The fast path is 3 steps (spec, gate, activate) or ceremony has crept in.
- Ceremony is proportional to blast radius, never to mood. `read` = fast
  path. `write|spend|prod` = full path with devil + gatekeeper.
- A method step exists only if its artifact is consumed by someone. No
  consumer, delete the step.
- Merge the engine, keep the frequent verbs as short entry points. A hub is
  a shared backend with many doors, not one door with modes.
- Rare verbs get a smart default, not an argument (bare `resume` = last
  save of this scope).

## Creation and governance

- The factory is the single entry point of agent creation. Out-of-band
  creation is discouraged by the write-deny rules and caught at the commit
  boundary (CI + branch protection).
- Gates check form; the fresh-eyes devil checks substance; the gatekeeper
  judges opportunity. One human point, full path only.
- A card committed to git is gate-green. Work-in-progress stays in the tree.
- Durable artifacts ship without LLM tells: gate_slop sweeps the
  wiki against `slop/slop-rules.csv`. The mechanism ships; an org's own
  rule corpus plugs in and stays private.
- Rules are enforced at the harness level, amendable only through
  `flows/amend-rule.md`. Inviolable in execution, a constitution not a dogma.
- Every change verifies its global impact before it lands: dedup and
  conflict-check against what exists, amend the existing rather than stack a
  second one beside it, leave the whole coherent not just the diff correct. A
  local change blind to the global is a cigarette butt in the forest.
  gate_antidup, the gatekeeper conflict motif and the consumption test are
  instances of this one law (ADR-020).

## Forms and layers (an estate is not all agents)

- A gate installed on a host repo governs only what the agents PRODUCE
  (wiki/), never the host's own pre-existing files.
- A signal heuristic over human prose must handle negation (never/no/not);
  it is a tripwire, the devil and gatekeeper are the real guard.

- Classify an artifact's form before its fate: agent (acts), data-source
  (read), tool (called), doctrine (injected). A wiki filed as a skill is a
  data-source, not an agent to merge.
- A source of truth read by many consumers stays a shared layer; never
  merged into one consumer.
- A context agent bound to a repo/mission is atomic. Never merge two
  missions. Source coupled to a SINGLE consumer may merge.
- The design system is a data-source with the wiki's compound loop:
  anti-dup a component before producing, stage it, gatekeeper promotes.
  Homogeneity is the by-product. Coding conventions are doctrine. Both are
  to be enforced by gate_design / gate_code (specified in ADR-016, not yet
  shipped).

## Capture and memory

- Two memories, governed oppositely: METHOD memory (rules, meta ADRs)
  distills and archives, so nobody reads a library to act. WORK memory
  (project ADRs, learnings, bugs, saves: who did what and why) accumulates
  forever, append-only and attributed. Distillation touches method only;
  work is the product, capture it whole.

- Delivery IS the save: work built or shipped is consigned by the act itself
  (the commit is the save, the git log the journal). Produced work is never
  "to save later". Trace a decision's atom AT RESOLUTION so its why is
  delivered too; the raw transcript covers raw data loss (ADR-019).
- For the residue delivery cannot cover (unfinished work's resume point), a
  condensed save is a FALLBACK, not the mechanism: proposed on an objective
  trigger (context pressure AND unlogged consumable since the last save, one
  nudge per threshold, reserving a save's own token cost as headroom). A
  pre-commit check for that miss is specified but not yet shipped; meanwhile the
  user may save anytime.
- Adoption is lossless: copy first, wrap never rewrite, originals kept.
- Traceability is a VIEW derived from git, never a fourth registry. The
  vocabulary is locked: INDEX indexes atoms, REGISTER indexes saves, LEDGER
  logs governance events, `gates/trace.py` PROJECTS git into commit-to-atom
  links on demand. A commit that lands an atom names it in its message, so
  blame to SHA to atom to the full why is one walk (ADR-020/021).
- Doc that DESCRIBES repo state is generated, never hand-typed: it lives
  between markers, `gates/docgen.py` fills it from the source, `gate_docs`
  fails the commit if the frozen text drifts. The README is a spreadsheet
  (formula plus freshness gate), not a document that rots. Narrative doc (the
  why) is edited in the commit that changes it, never on a schedule (ADR-022).
- The system measures itself: prevention is counted at the source
  (the ledger), ROI is a before/after diff, not an opinion.
- The per-author digest counts contributions, never judges people. It is
  for recognition and learning; a scoreboard that punishes empties itself
  (Grudin). The framework refuses to rank people.

## Install and distribution

- Install is one command, `uvx microwave-method` (uv is the Python npx): a
  self-contained, stdlib-only package that copies the files, seeds the wiki,
  wires the hook, then hands off to the agent for the guided welcome. The core
  stays Python because the value is zero-dependency; distribution follows the
  core, never a second runtime like Node (ADR-024).

## Guidance and onboarding

- Discovery precedes the plan; its depth follows the clarity of the intent, not
  mood (like the ceremony selector). One to three questions by default, escalate
  to `techniques/` brainstorming only when the user cannot formulate, never
  block someone who knows what they want.
- Guided flows adapt to the person, detected or slipped into one phrase, never a
  frontal questionnaire: language (theirs, followed not asked), register (plain
  by default per Nielsen Norman, expert opt-in via a shown A/B choice not
  self-rating), scale (attribution off in solo, automatic and git-sourced in a
  team). Fluidity overrides: every question earns its place, never a wall.
- Creation offers the body plainly ("want this as a desktop app, icon and
  shortcut?"): default yes for a powerful agent (identity), a real option for a
  read-only one (ADR-004/023). Never a silent side effect.

## Embodiment

- An agent that can do damage (write/spend/prod) must have a desktop body
  before activation. A read-only throwaway agent may stay bodiless.

---
Each rule traces to an ADR/LRN in `wiki/adr/` and
`wiki/projects/microwave/learnings/` for the reasoning. Read those only
when you need the why; this file is the what.
