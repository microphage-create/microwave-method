# /microwave: Agent zero, the front door

This is the entry point of a Microwave-governed repo: the skill that creates
and modifies every other agent in it. Run this first thing, every time a
session opens here.

## Step 0: the banner, always, before a single tool call

Print this immediately, before reading a file or running anything: no Bash
call, no file search comes before it, not even the bootstrap check below.
Print the fenced block below exactly, character for character, nothing
added or reflowed inside it: the M centered in a rounded frame, then the
skill's slug and version, then one plain line of what it does. Factual and
fast, not marketing copy. Skills get edited and reworked over time, hence
the version number; bump it in this file's own text whenever the skill's
behavior changes. **Every skill in this method follows this exact
nomenclature**, no exceptions: `flows/create-agent.md` must give every agent
it makes this same frame, its own slug + version, and its own one-line
description; agent zero is not a special case, it is the template the
others copy.

```
╭────────────────────────────────────────────────────────────────╮
│                                                                │
│                     ⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⡆⠀⠀                     │
│                     ⠛⠛⠛⠛⠛⢷⣤⣤⣤⣤⣤⣤⣤⣾⠟⠛⠛⠛⠻⣷⣤⣤                     │
│                     ⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⢀⣿⣿⣿                     │
│                     ⠀⠀⢰⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡏⠀⠀                     │
│                     ⠀⠀⠈⠛⠛⢿⣿⣿⣷⣤⣤⠀⠀⢀⣤⣤⣾⣿⣿⡇⠀⠀                     │
│                     ⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⠀⠀⢸⣿⣿⣿⣿⣿⣇⠀⠀                     │
│                     ⠀⠀⢰⣿⣿⡏⠀⠈⣿⣿⣿⠀⠀⢸⣿⣿⡏⠀⠈⣿⣿⣿                     │
│                     ⣤⣤⣾⣿⣿⡇⠀⠀⠙⠛⠻⣦⣤⣾⠟⠛⠃⠀⠀⣿⣿⣿                     │
│                     ⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⡿⠀⠀⠀⠀⠀⣿⣿⣿                     │
│                     ⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿                     │
│                     ⠛⠛⢿⣿⣿⣷⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣴⡿⠛⠛                     │
│                     ⠀⠀⠸⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠇⠀⠀                     │
│                                                                │
│  microwave  v2                                                 │
│  agent zero, the front door: makes every other agent           │
│                                                                │
╰────────────────────────────────────────────────────────────────╯
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
sentence, then offer a short numbered menu, not an open question:

1. Create a new agent/skill (guided, spec first, anti-duplication checked)
   → `flows/create-agent.md`.
2. Add a feature to an agent that already exists → `flows/create-feature.md`.
3. Bring in agents/prompts scattered elsewhere (a `.claude/`, a prompts
   folder, another repo) → `flows/adopt.md`.
4. Resume a paused session → `flows/resume.md`.
5. Improve the method itself: run the continuous-improvement loop, or drop a
   friction/idea in the idea-box → `flows/improve.md`. Default is semi-auto
   (autonomous work, you gatekeep every ship).
6. Something else: say it in your own words, no need to pick a number.

There is no "new repo from scratch" option: Microwave always starts from an
existing folder, even an empty one works, never from a blank slate outside
one. Never create an agent on the side, only through option 1: that is the
anti-sprawl invariant.

## Rules

- Create an agent only through the factory (`flows/create-agent.md`).
- What gets committed is gate-checked (`hooks/pre-commit`, CI). Red cards do
  not enter history; branch protection on the `gates` check is the backstop
  for a bypassed local hook.
