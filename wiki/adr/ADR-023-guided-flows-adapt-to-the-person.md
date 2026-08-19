---
type: adr
id: ADR-023
title: Guided flows adapt to the person, fluidity first
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-023: Guided flows adapt to the person, fluidity first

## Context

The first five minutes decide adoption, and the same flow serves a novice and
an expert, a solo developer and a two-thousand-person org, a French speaker and
an English one. A one-size flow loses most of them: too much hand-holding bores
the expert, too little abandons the beginner at the first friction. Claude's
plan mode is too light for this (no calibration, no persistence, no discovery),
and heavyweight agent methods put a long brainstorming ceremony in front of
everyone. We want the middle: a guided flow that reads its audience and adapts,
staying light.

## Decision

- Discovery precedes the plan, and its depth follows the CLARITY of the intent,
  not the mood (the same selector shape as blast radius, ADR-003). Default: one
  to three targeted questions. Escalate to brainstorming (`techniques/`) only
  when the user cannot formulate the intent (a vague one-word ask, "I don't
  know", contradictory answers, several live readings after a re-ask, or an
  explicit request for help). Never block someone who knows what they want.
- Calibrate the register by a SHOWN preference, not self-rating: offer the same
  sentence in two voices (A expert, B plain) and read the choice. People rate
  their own level badly; a shown preference is honest.
- The whole flow then adapts to that profile, and all of it is detected or
  slipped into one phrase, never a frontal questionnaire:
  - Language: the user's language, followed from how they write, never asked
    (the executing agent is multilingual). The framework's own files stay
    English; the conversation is localized.
  - Register: plain by default (Nielsen Norman: plain language beats expert
    prose for comprehension), expert as an opt-in, reversible at any moment.
  - Scale: attribution is off and invisible in solo (useless friction), and in
    a team it signs what is produced automatically, reusing the git identity of
    each commit (ADR-018/021), never a new login. Ask a name or role only if
    the team case is real and git does not already carry it.
- Creation offers the body plainly, it does not impose it opaquely: when an
  agent is created, the flow asks "want this as an app on your desktop, with its
  icon and shortcut?" (embodiment, ADR-004). For a powerful agent the body also
  serves identification, so it is the default yes; for a read-only helper it is
  a genuine option. Either way it is a clear proposal, never a silent effect.
- Fluidity overrides everything: every question must earn its place, never a
  form, never a wall, it flows. When fluidity and completeness conflict on the
  onboarding path, fluidity wins; the expert path may be denser.

## Consequences

`flows/welcome.md` implements this; discovery becomes a reusable phase the
creation flows prefix instead of each re-eliciting. Register, language, and
scale are session parameters set once and applied throughout. The honest limit:
adaptation quality depends on the executing agent, because Microwave is a method
and not a runtime; the flow is written explicitly to maximize it whatever the
agent. Plain-by-default is a deliberate stance, not a limitation, and it is
always reversible.

## Links

[[ADR-003-ceremony-selector]] [[ADR-004-embodiment]] [[ADR-018-contribution-digest]] [[ADR-021-traceability-is-a-git-projection]]
