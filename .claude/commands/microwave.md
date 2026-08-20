# /microwave — Agent zero, the front door

This is the entry point of a Microwave-governed repo: the skill that creates
and modifies every other agent in it. Run this first thing, every time a
session opens here.

## Step 0: bootstrap, if you are not installed yet

This skill file can exist on its own, dropped into a fresh repo before
anything else. Check: does `gates/gate_wiki.py` exist here? If not, you are
running before the rest of Microwave landed. Run `uvx microwave-method` via
Bash right now (installs from PyPI, no separate step for the person), let its
wizard finish (files, desktop icon, Windows Terminal profile), then continue
below in the same session. Never tell the person to go run a command
themselves and come back: you drive the whole thing, start to finish.

## Startup

1. Read `wiki/INDEX.md`, the registry: one line per agent, who does what.
2. Skim the headings in `wiki/adr/`: the decisions that bind this repo.

That is the whole ceremony: seconds, not an interrogation.

**Fresh install check.** If the Agents section of `wiki/INDEX.md` lists only
`microwave` and nothing else, the CLI wizard finished but the guided part
never ran: this is a first session after install. Don't announce it, don't
ask first, just start `flows/welcome.md` right now, before the user has
typed a word. You drive, the user only answers simple questions and says yes.

**Otherwise**, you are contextualized. Say what's registered in one plain
sentence, then ask what we are building. From here:

- New agent? Run `flows/create-agent.md`. Never create one on the side, that
  is the anti-sprawl invariant.
- Onboarding an existing folder of prompts/skills? Run `flows/adopt.md`.
- Anything else: proceed normally, the registry and ADRs above are your
  context now.

## Rules

- Create an agent only through the factory (`flows/create-agent.md`).
- What gets committed is gate-checked (`hooks/pre-commit`, CI). Red cards do
  not enter history; branch protection on the `gates` check is the backstop
  for a bypassed local hook.
