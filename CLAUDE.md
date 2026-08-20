# CLAUDE.md: this repo runs on Microwave

Microwave governs how agents get made here and what they remember. On session
start, before anything else, get your bearings so you are never wired to
nothing:

1. Read `wiki/INDEX.md` — the registry. One line per agent: who does what.
2. Skim the headings in `wiki/adr/` — the decisions that bind this repo.

That is the whole ceremony: seconds, not an interrogation. Now you are
contextualized.

- Create an agent only through the factory (`flows/create-agent.md`), never on
  the side. That is the anti-sprawl invariant.
- New here? `flows/welcome.md` takes you by the hand.
- What you commit is gate-checked (`hooks/pre-commit`, CI). Red cards do not
  enter history; a determined committer can still bypass a local hook, which is
  why branch protection with the `gates` check is the backstop.
