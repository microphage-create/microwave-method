# Flow: welcome (guided onboarding, take the user by the hand)

The first five minutes decide adoption. Most people abandon a tool at the first
friction, so this flow removes every decision the user should not have to make.
You, the coding agent, run it right after install: you drive, the user only
answers simple questions and says yes. It does not re-implement anything; it
orchestrates `adopt` and `create-agent` with a human at the wheel.

## The one rule of this flow

Fluidity above everything. Every question must earn its place; never a form,
never a wall, it flows. One action at a time, never a blank prompt. After every
step, say what just happened in one plain sentence, then propose the next action
with a default the user can accept by just agreeing. Never show jargon, a stack
trace, or an internal id unless asked. Always offer a clean stop: "we can stop
here and pick up later with the resume flow."

## Step 0: Check the ground, reassure (never crash)

Confirm the basics quietly and fix or explain, do not fail in their face:

- Not a git repo? Offer: "This folder is not a git project yet. Want me to run
  `git init`? (recommended)."
- `python` / `python3` missing? Give the single install line for their OS, wait.
- Run `python gates/gate_wiki.py` once. Green: "Microwave is installed and
  healthy." Not green: read the message and fix it for them, do not show it raw.

Report readiness in one friendly sentence. Do not list what you checked.

## Step 1: Calibrate to the person, in one fluid question

Do not ask "are you a beginner or an expert" (nobody rates themselves well).
Show the choice and read which one they pick:

> Quick thing so I match how you like to work. Which sounds better?
> A) "I'll scan your `.claude/` directory and index your agents into the registry."
> B) "I'll look at the tools you already have and make you a clean list."

A leans expert: keep the vocabulary, go denser, explain less. B leans plain: no
jargon, name things by what they recognize, explain a little more, hold their
hand more. Set the whole flow's register from that one answer, and say they can
switch anytime ("tell me 'go simpler' or 'go expert' whenever"). One question,
no form, it flows.

Then, in that register: "Microwave maps the agents you already have and brings
them under one roof, one at a time. First I just look, nothing is changed or
deleted. Ready?" Wait for yes.

## Step 2: The first scan (delegate to adopt)

Run `flows/adopt.md`. Ask only the one question it needs ("where do your agents
live: a `.claude/` folder, a prompts folder, a repo?"), prefilled with guesses
from what you can already see in the working tree. Do the scan. Present the
result as a short human summary: "I found N things: X agents, Y notes, Z that
look dead. Here they are, most-used first." Show the backlog readably, not the
raw file.

## Step 3: Read the map together

Explain the choices in plain words, not the vocabulary: "For each one we can
bring it in, fold it into another, leave it alone for now, or retire it. I have
pre-proposed a choice for each. Want to change any, or shall we start with the
top one?" The user prunes by talking, not by editing a file.

## Step 4: The first agent, hand in hand (delegate to create-agent)

Take the top item to bring in and run `flows/create-agent.md` with its archive
entry as the elicitation input. Narrate lightly: "I am recreating <name>
through the factory: this runs the checks, and because it can act, it gets an
icon and its own terminal." On the fast path do not stop; on the full path,
surface only the decisions that are genuinely the user's (the gatekeeper
moment), never the mechanics.

## Step 5: First win, then the door stays open

When the first agent activates: "Done. <name> is governed and has an icon on
your desktop. That is the whole loop, and every next agent is the same three
steps." Then hand back control: "You can keep going now, stop and resume
anytime, or run the whole backlog at your own pace. What would you like?"

## When something breaks (the user is not a debugger)

Never surface a raw error. For each common failure, state the cause and the fix
in one sentence, then offer to do it:

- permission denied on a hook or file: offer the exact fix, or skip the hook and
  continue (the CI gate still guards).
- no `.claude/` or prompts found: "Looks like a fresh start, nothing to adopt.
  Want to create your first agent from scratch instead?" and go to Step 4.
- a gate rejects during creation: translate the message ("the card is missing
  X"), fix it, re-run. The user never sees the gate output raw.

The measure of this flow: the user reaches their first governed agent without
once being asked something they could not answer, and without once seeing
something break with no way forward.
