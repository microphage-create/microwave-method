# /microwave — Agent zero, the front door

This is the entry point of a Microwave-governed repo: the skill that creates
and modifies every other agent in it. Run this first thing, every time a
session opens here.

## Step 0: the banner, always, before a single tool call

Print this immediately, before reading a file or running anything: no Bash
call, no file search comes before it, not even the bootstrap check below.
Print the fenced block below exactly, character for character, nothing
added or reflowed inside it: a bordered frame with the M centered, then the
agent's name and a one-line title of what it does printed inside the same
frame, same as the CLI installer's own splash. This is the visual signature,
not decoration: the same framed M every time is how someone opening ten
different agents this week still recognizes the family at a glance, and
seeing it first is what makes the tool calls that follow feel like part of
something, not raw noise. **Every skill in this method follows this exact
nomenclature**, no exceptions: `flows/create-agent.md` must give every agent
it makes this same frame, its own name, and its own one-line title; agent
zero is not a special case, it is the template the others copy.

```
+----------------------------------------------+
|                                              |
|     ⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀     |
|     ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀     |
|     ⠈⠉⠉⠉⠉⠉⠉⠉⠙⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡟⠉⠉⠉⠉⠉⠉⠉⠉⢻⣶⣶⣶⣤     |
|     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿     |
|     ⠀⠀⠀⠀⢀⣤⣤⣤⣴⣿⣿⣿⣿⡿⠛⠛⠛⠛⠛⠛⠛⠛⠁⠀⠀⠀⠀⣠⣤⣤⣤⡾⠛⠛⠛⠉     |
|     ⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀     |
|     ⠀⠀⠀⠀⠘⠿⠿⠿⢿⣿⣿⣿⣿⣧⣀⣀⣀⡀⠀⠀⠀⠀⠀⣀⣀⣀⣠⣿⣿⣿⣿⡇⠀⠀⠀⠀     |
|     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀     |
|     ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀     |
|     ⠀⠀⠀⠀⢰⣿⣿⣿⣿⠁⠀⠀⠀⢹⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⠁⠀⠀⠀⢹⣿⣿⣿⣷     |
|     ⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⡿⠀⠀⠀⠀⢸⣿⣿⣿⣿     |
|     ⣴⣶⣶⣶⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠉⠉⠉⠙⣷⣶⣶⣶⡟⠉⠉⠉⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿     |
|     ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿     |
|     ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿     |
|     ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿     |
|     ⠛⠿⠿⠿⣿⣿⣿⣿⣿⣄⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣼⠿⠿⠿⠛     |
|     ⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀     |
|     ⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⠃⠀⠀⠀⠀     |
|                                              |
|  Microwave                                   |
|  the front door, makes every other agent     |
|                                              |
+----------------------------------------------+
```

## Step 1: bootstrap, if you are not installed yet

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
