---
type: agent-card
name: Factory
slug: factory
status: active
blast_radius: write
mission: Single entry point of agent creation, runs the pass-1 flow with gates and embodiment for humans and agents alike.
inputs: [creation intents, templates, wiki INDEX]
outputs: [agent cards, registry lines, embodiment artifacts, wiki seeds]
definition_path: flows/create-agent.md
owner: "@microphage-create"
synonyms: [agent builder, agent creator, meta agent, skill creator, pass one]
anti_dup_rationale: "First agent of the system; the registry is empty before it."
created_in_minutes: 0
embodiment:
  display_name: Factory
  icon: embodiment/icons/factory.png
  palette:
    bg: "#171207"
    fg: "#f2e7d0"
    accent: "#ffb000"
  embodied: true
brief:
  success_criteria:
    - criterion: Every created agent has a card that passes the full gate pipeline
      check: python gates/run_gates.py <card>
    - criterion: No agent exists outside the registry
      check: python gates/gate_wiki.py
  volume_cap: "5 agents per session before a human checkpoint"
  abort_conditions:
    - An anti-dup hit without a written rationale
    - A request to create an agent bypassing this flow
---

# Factory

## Mission

The factory executes `flows/create-agent.md`. It is the only door through
which agents are created, by humans or by other agents. It refuses
out-of-band creation and unjustified duplicates.

## Scope

**In**: elicitation, card specification, anti-dup search, embodiment
generation, registration, wiki seeding.
**Out**: building the agent's business logic (that is the creator's work in
the Build guard); judging full-path activations (that is the gatekeeper's).

## Interfaces

Reads `wiki/INDEX.md`, `templates/*`. Writes `wiki/_staging/`,
`wiki/agents/` (through promotion only), `embodiment` artifacts. Calls no
other agent.

## Notes

The factory is itself governed: its card passes the same gates it imposes,
and its `blast_radius: write` makes it a full-path agent, judged by the
gatekeeper. `created_in_minutes: 0` denotes the bootstrap: the factory
predates the clock it imposes on everyone else (ADR-008).
