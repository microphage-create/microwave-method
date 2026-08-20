# Registry index

One line per artifact. Humans scan it, LLMs load it, `gate_antidup` searches
it, the runtime resolves agents through it. A line has the form:

`- [type] id: one-line summary → path`

## Agents

- [service] librarian: Curate the wiki between gatekeeper sessions by proposing promotions, flagging rot, and keeping links and index coverage healthy → wiki/agents/librarian.md

- [service] factory: single entry point of agent creation, runs the pass-1 flow with gates → wiki/agents/factory.md
- [service] microwave: agent zero, the desktop front door that opens a context-loaded session on this repo → wiki/agents/microwave.md

## Rules and rationale

- Live rules (the what): `wiki/RULES.md`
- Archived rationale (the why), opened on demand: ADRs (`wiki/adr/`, meta, distilled and time-limited) and learnings (`wiki/projects/microwave/learnings/`, product work, append-only)


## Projects

- [project] microwave: the framework itself, first product-plane project → wiki/projects/microwave/brief.md
