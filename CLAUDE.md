# CLAUDE.md: this repo runs on Microwave

Microwave governs how agents get made here and what they remember. On session
start, before anything else, get your bearings so you are never wired to
nothing:

1. Read `wiki/INDEX.md`, the registry: one line per agent, who does what.
2. Skim the headings in `wiki/adr/`: the decisions that bind this repo.

That is the whole ceremony: seconds, not an interrogation. Now you are
contextualized.

**Fresh install, second half.** If the Agents section of `wiki/INDEX.md` lists
only `microwave` and nothing else, the CLI wizard finished but the guided part
never ran: this is a first session after install. Don't announce it, don't ask
first, just start `flows/welcome.md` right now, before the user has typed a
word. You drive, the user only answers simple questions and says yes.

- Create an agent only through the factory (`flows/create-agent.md`), never on
  the side. That is the anti-sprawl invariant.
- New here? `flows/welcome.md` takes you by the hand.
- What you commit is gate-checked (`hooks/pre-commit`, CI). Red cards do not
  enter history; a determined committer can still bypass a local hook, which is
  why branch protection with the `gates` check is the backstop.
