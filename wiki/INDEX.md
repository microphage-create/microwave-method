# Registry index

One line per artifact. Humans scan it, LLMs load it, `gate_antidup` searches
it, the runtime resolves agents through it. A line has the form:

`- [type] id: one-line summary → path`

## Agents

- [agent] librarian: Curate the wiki between gatekeeper sessions by proposing promotions, flagging rot, and keeping links and index coverage healthy → wiki/agents/librarian.md

- [agent] factory: single entry point of agent creation, runs the pass-1 flow with gates → wiki/agents/factory.md

## Rules and rationale

- Live rules (the what): `wiki/RULES.md`
- Archived rationale (the why, ADRs + learnings, distilled and time-limited): `wiki/adr/` and `wiki/projects/microwave/learnings/`


## Projects

- [project] microwave: the framework itself, first product-plane project → wiki/projects/microwave/brief.md
