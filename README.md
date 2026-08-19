# Microwave Method

**An agent factory with a governed memory. Heavy pass once per agent, light pass per feature. Context is cooked once and reheated at cache price.**

*Methods tell you what to do. Microwave gates how agents get made, and governs what they remember.*

[![gates](https://github.com/microphage-create/microwave-method/actions/workflows/gates.yml/badge.svg)](https://github.com/microphage-create/microwave-method/actions/workflows/gates.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

```bash
uvx microwave-method
```

**In one breath:** create AI agents and keep them mappable. Machine gates
enforce the FORM of every creation, a human gatekeeper plus an
adversarial pass review the substance, and a governed wiki of atoms (readable, not an opaque vector store)
is the compounding memory.

Microwave is a method, not a runtime. It ships as markdown flows, templates, and
a handful of dependency-free scripts that any coding agent (Claude Code, Codex,
Cursor, ...) can execute. It answers one question organizations keep failing at:
**how do you let everyone create agents without ending up with a pile of agents
nobody can map?**

> Gartner projects that [enterprise apps embedding task-specific AI agents jump
> from under 5% in 2025 to 40% by 2026](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025),
> and, separately, that [more than 40% of agentic AI projects will be canceled by
> the end of 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027).
> Agents multiply faster than anyone maps them, and most never make it. Microwave
> is the missing discipline underneath: rules for who creates agents, a central
> inventory, and a lifecycle that retires the dead. Open source you install in
> your repo, not a SaaS you buy.

Scope, precisely: the governed memory and the anti-dup registry live in a repo,
so each repo gets its own clean, git-native registry. An agent is not locked to
one, though: install Microwave in as many repos as you want, and a
contextualizing agent can span several. Cross-repo anti-dup (a shared or
federated registry) is a natural extension, not a wall; the per-repo discipline
is the layer an enterprise-wide rollup builds on, not a ceiling.

## Why "Microwave"

A microwave oven does not cook your dish from scratch. It excites the water
molecules already present in it. That is the whole thesis: **your wiki atoms are
the water molecules.** The expensive work (specifying an agent, curating what it
learned) is done once and stored. Every subsequent feature just reheats context
that already exists, at cache-read price, instead of rediscovering it from
scratch on every session.

## The middle you were missing

```
  HEAVY FRAMEWORKS       |   >>  MICROWAVE  <<   |             PLAN MODE
  SAFe, epics, PRDs      |     the real agile    |          just-in-time
  -----------------------+-----------------------+----------------------
  hours of ceremony      |  minutes, no meeting  |               seconds
  sprints & rituals      |     machine gates,    |        no ritual, and
  nobody believes in     |     not committees    |      nothing survives
  docs nobody rereads    |   light AND governed  |           the session
  governance = process   |   distills, no bloat  |         no governance
  compounds, but heavy   |  compounds, and light |       never compounds
  -----------------------+-----------------------+----------------------
                           the middle, by design,
                           not by promise
```

Agile began as a light manifesto: working software over documentation, responding
to change over following a plan. Enterprises turned it into SAFe, story points,
epic grooming and sprint rituals nobody believes in: bureaucracy wearing agile's
badge. Microwave is the return to the real thing. Ceremony is proportional to what
an agent can actually break, an artifact exists only if something consumes it, and
the checks are machine gates, not meetings. Light like the original agility,
governed like the heavy frameworks, compounding like neither. No epics, no
committee, no ritual for ritual's sake.

Two mechanical tests make it the middle by construction, not by promise:

1. **The consumption test.** A method step exists only if its artifact is
   consumed by someone: the runtime, the registry, or the gatekeeper. A step whose
   output nobody reads is deleted from the method.
2. **The ceremony selector.** The depth of the creation flow is proportional to
   the agent's blast radius (what it can read, write, spend, or touch), never to
   the creator's mood. Read-only helper: fast path, minutes. Agent that writes,
   spends, or touches production: full path, with a human gatekeeper before
   activation.

## How it works

One recursive method, two planes, one registry.

```
        META PLANE (the factory)           PRODUCT PLANE (the work)
  +----------------------------------+   +----------------------------------+
  | PASS 1: heavy, ONCE per agent    |   | PASS 2: light, EVERY feature     |
  | elicit -> spec -> anti-dup ->    |   | intent -> a short story with     |
  | build -> embodiment -> card      |-->| verifiable done-criteria ->      |
  | in the registry, wiki seeded     |   | build -> traces to the wiki      |
  +----------------------------------+   +----------------------------------+
                    ^                                      |
                    '-- governed promotion (gatekeeper) ---'
```

- **The registry** is an index-first file: one line per agent, cards opened on
  demand, readable by humans and by LLMs. A registry the agent reads on demand,
  not a doc set nobody reopens, is far harder to let rot.
- **The wiki** has one format and two scopes: `wiki/agents/` +
  `wiki/adr/` (org-wide meta plane) and `wiki/projects/<name>/` (product
  plane). Learnings are promoted upward only through the gatekeeper. Subsidiarity:
  every atom lives at the lowest level that suffices.
- **Recursion is governed.** Agents may create agents, but only through the
  factory: the factory is the single entry point of creation. That is the
  anti-sprawl invariant.

## The loop, in one glance

It opens with elicitation, a few questions to pin the intent, escalating to a
bank of brainstorming methods when the intent is fuzzy. Then the governed half:
one entry point, automatic quality gates, and a human guardrail that doubles as
decision support. At the heart sits the LLM wiki, your second brain, atoms
readable by human and machine, opened by exact id rather than fuzzy RAG. The loop
feeds the wiki; the wiki reheats and informs the next pass.

```
            YOUR INTENT
                 |
                 v
  +----------------------------------+
  |   ELICITATION: a few questions   |      clear intent -> 1-3 questions.
  |  stuck? -> the BRAINSTORM bank   |      a library of thinking methods
  +----------------------------------+      (the techniques/ data)
                 |
                 v
   ONE ENTRY POINT: THE FACTORY             nobody creates on the side
                 |
                 v
  +----------------------------------+
  |    QUALITY GATES (automatic)     |      duplicate? jargon? testable?
  +----------------------------------+
       read |       | write / spend / prod
            |       v
            |   ADVERSARIAL REVIEW          a fresh agent attacks it,
            |   + HUMAN GATEKEEPER          then a human decides (decision support)
            v       v
  +----------------------------------+
  |   THE REGISTRY: 1 line / agent   |      who does what, searchable
  +----------------------------------+
                 |
          [ the agent works ]
                 |
                 v
  +==================================+
  |      THE LLM WIKI  (atoms)       |      << YOUR SECOND BRAIN >>
  |   1 idea = 1 atom, plain text    |      readable by human AND machine
  |    linked, indexed, governed     |      opened by exact id, not fuzzy RAG
  +==================================+
                 |
   reheated at cache price + informs the next decision
                 |
                 '--> feeds the next elicitation & build --.
                                                           |
   .-------------------------------------------------------'
   '--> THE LOOP: the wiki is the brain. Each pass makes it
        richer, and the next pass cheaper and better-decided.
```

A real creation, end to end:

```
You: "I want a skill that reads my contracts and flags risky clauses"

  1. The factory asks two questions
     - read only, or does it write/send?  -> read only
     - where are the contracts?           -> the /contracts folder

  2. It writes the card: mission, scope, verifiable success criteria

  3. Quality gates run (2 seconds, automatic)
     [ok] no duplicate of an existing agent
     [ok] the card conforms
     [ok] the criteria are testable

  4. Read-only, so fast path: activated on the spot
     (wrote or sent anything -> adversarial review + a human approves first)

  5. Filed in the registry (one line, searchable). Read-only, so it stays
     bodiless; a write/spend/prod agent would also get a desktop icon + terminal

  -> Three minutes. The next skill of this kind starts from this card, not zero.
```

## The memory is a wiki, not a vector store

Most tools make the vector store the memory itself: chop your docs into chunks,
turn each into an opaque vector, and at query time pull back "whatever looks
similar". As a substrate it half-works and rots invisibly: chunks are cut
mid-thought, nobody can read a vector, and nothing is governed, so a stale or
wrong chunk lives forever. The problem is not that search is bad; it is that an
unreadable, ungoverned store has become the memory.

Microwave's memory is a governed wiki of atoms: atomic notes in the Zettelkasten
lineage, the shape Andrej Karpathy has argued LLMs should keep their knowledge
in. One atom is one idea, in plain markdown, tagged (type, id) and linked to the
others.
Three things follow:

- **Readable both ways.** The same file serves the human, who reads and corrects
  it, and the agent, which opens it on demand. One source of truth, not a doc set
  for people plus a vector store for the machine. You can see, in plain text,
  what your system knows.
- **Targeted, not fuzzy.** A compact index lets the agent scan what exists and
  open the atom it needs by name, instead of hoping a similarity search surfaced
  the right chunk. The agent still chooses, so it is not magic, but it chooses
  from named, readable entries, not opaque vectors. Excite the right molecule,
  do not reheat the whole pan.
- **Governed and alive.** The gates refuse duplicates, doctrine distills instead
  of piling up, and wikilinks turn atoms into a graph, a real body of knowledge.
  This is the second brain of your whole workflow: a persistent external memory
  your agents query, not a throwaway context reloaded blind every session.

Search is a separate layer, and modern retrieval is good at it: reranking,
metadata filters, hybrid search. It composes ON TOP of an atom wiki; it is not an
alternative to it. Keep the readable, governed atoms as the substrate and source
of truth; add retrieval over them when the corpus outgrows a scannable index.
Substrate first, search on top: right tool, right place.

## Gates, not meetings

A creation plan passes a series of **machine gates**, like a CI for agent
creation. No committee, no ceremony:

<!-- microwave:gates start -->
<!-- generated by gates/docgen.py, do not edit by hand -->

| Gate | Guarantee |
|---|---|
| `gate_antidup` | no unjustified overlap with the registry |
| `gate_brief` | the 3-section brief is complete |
| `gate_schema` | the agent card matches the template contract |
| `gate_testable` | every done-criterion names a check, and a framework gate it |
| `gate_embodiment` | the agent has a body when it needs one |
| `gate_slop` | durable artifacts do not read like slop |
| `gate_wiki` | the wiki is linked, indexed, and its atoms carry their contract |
| `gate_docs` | generated doc sections match their source |

<!-- microwave:gates end -->

This table is generated from the gates themselves by `gates/docgen.py` and
cannot go stale: `gate_docs` fails the build if it drifts from the code
(ADR-022). The slop bank (`slop/slop-rules.csv`) ships as a generic starter and
takes your org's own rows; the mechanism does not change.

Every gate rejects with an actionable message; you fix and re-run. Gates check
form; substance is attacked by the **devil loop** (`flows/devil-loop.md`): a
fresh agent session with no creation context reviews every full-path creation
adversarially, round after round, until it finds nothing. **One single human
point**: the gatekeeper, only on the full path, judging only cards with a
clean devil report. On the fast path, green gates = `gates/activate.py`,
nobody to wait for.

### What is actually enforced, and what is not

Stated plainly, because the difference matters.

**Structural** (a machine refuses; goodwill is not involved): the pre-commit
hook and the CI workflow (`.github/workflows/gates.yml`) run the gates and block
a commit that fails them. `CODEOWNERS` plus branch protection gate who can merge
to the protected space (you enable branch protection; the installer prints the
command). These exit non-zero. They are the real fence. The gates and the YAML parser they
rely on are covered by a stdlib test suite (`tests/`), run in that same CI.

**Cooperative** (the agent or harness has to play along): the flows, the
elicitation, the devil pass, and the gatekeeper's judgment are conventions the
method encourages, not code that exits non-zero. Whether a criterion's check
actually ran is the agent's honest report. The shipped permission deny-rules
(`harness/`) are an EXAMPLE, Claude-Code-specific, and cover the Read and Write tools (plus a token Bash rule),
not the shell in general, so a determined agent can still `cat` a file: treat them as a
hint, not a sandbox, and never as secret protection.

So Microwave hard-gates the FORM of what enters your repo, and makes the
substance reviewable (the devil pass, the human gatekeeper) rather than
guaranteed. Rules are amendable only through process (`flows/amend-rule.md`): a
constitution, not a dogma.

## Agents as apps

An agent that can do damage is not done until it has a body; a read-only one
may stay bodiless, with one deliberate exception: agent zero (Microwave itself),
the front door, is embodied at install so your desktop has a door to open. For a
powerful agent, pass 1 generates a desktop presence: an
icon, a short name, a themed terminal profile, a launcher. These
are **terminals dressed as apps, not apps replacing the terminal**: full
terminal power, zero anonymity. With five sessions open in parallel you know
who is who at a glance. One identity manifest, one adapter per OS
(Windows Terminal + PowerShell, iTerm2/Terminal.app, freedesktop). The
Windows adapter is the tested reference; **macOS and Linux adapters are
experimental (written, not yet run on real machines): testing one takes five
minutes and a report is a welcome first contribution.** See
`docs/embodiment.md`.

## Install (one command)

```bash
uvx microwave-method
```

One line, any OS, run inside the repo you want governed. Prerequisites: `git`,
Python 3.10+ and `uv` (the Python package runner, installs in one line); the
tool itself is standard-library-only. No `uv`? The shell bootstrap does the same
by cloning the repo (files, wiki, hook, CLAUDE.md, agent zero; the desktop icon
is uvx-only):

```powershell
# Windows (PowerShell 7+)
irm https://raw.githubusercontent.com/microphage-create/microwave-method/main/install/bootstrap.ps1 | iex
```
```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/microphage-create/microwave-method/main/install/bootstrap.sh | bash
```

The bootstrap clones `main` (unpinned) and runs the shell installer
(`install.sh` / `install.ps1`); prefer
`uvx microwave-method`, which pulls a specific published version, and read any
script before you pipe it to a shell. Per-OS walkthrough, troubleshooting and
uninstall: `docs/install.md`. The
generated reference (flows, gates, decisions) is `docs/reference.md`.

This copies the flows, templates, technique banks, slop rules, gates,
embodiment tooling, harness examples and hooks into your repo and seeds the
wiki, and drops the CI workflow, a CODEOWNERS placeholder, a session-start
CLAUDE.md, and the agent-zero card. On the `uvx` path,
the side effects (git setup, wiring the pre-commit hook, opening the welcome
flow) run only after you confirm: nothing touches your machine without a yes.
The piped shell bootstrap cannot prompt (its stdin is the script), so it wires
the hook directly, additively, backing up any existing pre-commit. Finish the
hardening by enabling branch protection (the installer prints the command).

If it did not open on its own, start it: in your coding agent, say
*"run the Microwave welcome flow"*. It takes you by the hand, adapts to you, and
scans wherever your agents sleep (`.claude/`, prompt folders, repos), archiving
one inventory entry per artifact found and writing the shopping list of
migrations (`wiki/_archive/BACKLOG.md`). Migrating an archived agent through
*"run the Microwave create-agent flow"* is the cheapest creation you will ever
run: the entry is the elicitation input. (Want the raw scan without the guided
wrapper? *"run the Microwave adopt flow"* does exactly that.)

## The economics, honestly

The honest version is unglamorous, so no headline percentage:

- Reading context is a large, repeated share of agent cost. A session that
  re-derives what an earlier one already figured out pays for it again.
- Prompt caching cuts the cost of re-reading the SAME context inside your
  provider's cache window (a read is a fraction of a write), so a stable, reused
  context file is cheaper on the second hit. The size of that win depends on the
  provider, the cache TTL, and the workload.
- The compounding win is separate and slower: not re-discovering knowledge
  across sessions and agents, because it was captured once as an atom and
  reopened by id instead of rebuilt. That is what the method automates.

We do not sell a number: the published figures on static context files are
contested, and yours depend on your setup. Measure your own instead. The method
instruments itself (`docs/method.md`), so diff your token spend before and after
on the same tasks.

## Status

Extracted from a system its author has run daily on a private stack, then
squashed and cleaned for release. The scale behind it (dozens of skills, a
multi-generation rule corpus) lives in that private system, not in this repo, so
take those as provenance, not proof. What this repo demonstrates on its own: it
self-hosts (its `wiki/agents/` pass the same gates the factory imposes) and it
passes its own gates. Judge it on that, and on what you build with it.

MIT. See `NOTICE.md` for attributions.

---

```
⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠈⠉⠉⠉⠉⠉⠉⠉⠙⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡟⠉⠉⠉⠉⠉⠉⠉⠉⢻⣶⣶⣶⣤
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿
⠀⠀⠀⠀⢀⣤⣤⣤⣴⣿⣿⣿⣿⡿⠛⠛⠛⠛⠛⠛⠛⠛⠁⠀⠀⠀⠀⣠⣤⣤⣤⡾⠛⠛⠛⠉
⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠘⠿⠿⠿⢿⣿⣿⣿⣿⣧⣀⣀⣀⡀⠀⠀⠀⠀⠀⣀⣀⣀⣠⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀    Microwave Method
⠀⠀⠀⠀⢰⣿⣿⣿⣿⠁⠀⠀⠀⢹⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⠁⠀⠀⠀⢹⣿⣿⣿⣷    an agent factory with a governed memory
⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⡿⠀⠀⠀⠀⢸⣿⣿⣿⣿
⣴⣶⣶⣶⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠉⠉⠉⠙⣷⣶⣶⣶⡟⠉⠉⠉⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿
⠛⠿⠿⠿⣿⣿⣿⣿⣿⣄⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣼⠿⠿⠿⠛
⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⠃⠀⠀⠀⠀
```
