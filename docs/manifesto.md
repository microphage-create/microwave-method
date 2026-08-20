# Manifesto

The long version. The README is the tool; this is the thinking behind it. Read it
if the short version made you curious, skip it if you just want to install.

## Why "Microwave"

The name has two readings, and both are the method.

**Micro-wave, the oven.** A microwave does not cook your dish from scratch; it
excites the water molecules already present in it. Your wiki atoms are the water
molecules. The expensive work (specifying an agent, curating what it learned) is
done once and stored, and every subsequent feature reheats context that already
exists, at cache-read price, instead of rediscovering it from scratch.

**Micro + wave, the ripples.** Small waves of continuous improvement. Each pass is
one small wave that leaves the wiki richer and the next pass cheaper and
better-decided. The loop is a swell, not a one-off.

Reheat and ripple: reuse what is already there, and let each pass raise the tide.

## The middle you were missing

```
  HEAVY FRAMEWORKS       |   >>  MICROWAVE  <<   |             PLAN MODE
  SAFe, epics, PRDs      |     the real agile    |          just-in-time
  -----------------------+-----------------------+----------------------
  hours of ceremony      |  minutes, no meeting  |               seconds
  sprints & rituals      |     machine gates,    |        no ritual, and
  nobody believes in     |     not committees    |      nothing survives
  docs nobody rereads    |   light AND governed  |           the session
  compounds, but heavy   |  compounds, and light |       never compounds
```

Agile began as a light manifesto: working software over documentation, responding
to change over following a plan. Enterprises turned it into SAFe, story points,
epic grooming and sprint rituals nobody believes in: bureaucracy wearing agile's
badge. Microwave is the return to the real thing. Ceremony is proportional to what
an agent can actually break, an artifact exists only if something consumes it, and
the checks are machine gates, not meetings. Light like the original agility,
governed like the heavy frameworks, compounding like neither.

Two mechanical tests make it the middle by construction, not by promise:

1. **The consumption test.** A method step exists only if its artifact is consumed
   by someone: the runtime, the registry, or the gatekeeper. A step whose output
   nobody reads is deleted from the method.
2. **The ceremony selector.** The depth of the creation flow is proportional to the
   agent's blast radius (what it can read, write, spend, or touch), never to the
   creator's mood. Read-only helper: fast path, minutes. Agent that writes, spends,
   or touches production: full path, with a human gatekeeper before activation.

## How it works: one recursive method, two planes, one registry

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
  demand, readable by humans and by LLMs. A registry the agent reads on demand, not
  a doc set nobody reopens, is far harder to let rot.
- **The wiki** has one format and two scopes: `wiki/agents/` + `wiki/adr/` (org-wide
  meta plane) and `wiki/projects/<name>/` (product plane). Learnings promote upward
  only through the gatekeeper. Subsidiarity: every atom lives at the lowest level
  that suffices.
- **Recursion is governed.** Agents may create agents, but only through the factory.
  Combined with the taxonomy (one context agent per repo, services shared), that is
  what keeps the set from sprawling.

## The loop, in one glance

It opens with elicitation, a few questions to pin the intent, escalating to a bank
of brainstorming methods when the intent is fuzzy. Then the governed half: one
entry point, automatic quality gates, and a human guardrail that doubles as
decision support. At the heart sits the LLM wiki, your second brain, atoms readable
by human and machine, opened by exact id rather than fuzzy RAG. The loop feeds the
wiki; the wiki reheats and informs the next pass.

```
   YOUR INTENT
        |
        v
   ELICITATION (a few questions; stuck? -> the brainstorm bank)
        |
        v
   ONE ENTRY POINT: THE FACTORY            nobody creates on the side
        |
        v
   QUALITY GATES (automatic)               duplicate? jargon? testable? uses resolve?
        |  read           |  write / spend / prod
        |                 v
        |            ADVERSARIAL REVIEW + HUMAN GATEKEEPER
        v                 v
   THE REGISTRY: 1 line / agent            who does what, searchable
        |
   [ the agent works ]
        |
        v
   THE LLM WIKI (atoms)                    << your second brain >>
        |
   reheated at cache price, informs the next decision, feeds the next build
```

A real creation, end to end:

```
You: "I want a skill that reads my contracts and flags risky clauses"

  1. The factory asks two questions
     - read only, or does it write/send?  -> read only
     - where are the contracts?           -> the /contracts folder
  2. It writes the card: mission, scope, verifiable success criteria
  3. Quality gates run (2 seconds, automatic): no duplicate, card conforms,
     criteria testable, declared services resolve
  4. Read-only, so fast path: activated on the spot
     (wrote or sent anything -> adversarial review + a human approves first)
  5. Filed in the registry (one line, searchable)

  -> Three minutes. The next skill of this kind starts from this card, not zero.
```

## The network: from microkit to macrokit

One install is a microkit: one person, one estate, governed. The interesting
property is that microkits compose.

- **Peer to peer, today.** A repo declares sibling repos in `.microwave/federation`,
  and the anti-dup checks a new agent against all of their registries at once, naming
  the repo that already holds an overlap. Services are shared across the federation:
  a context agent in one repo can wire a service defined in another. The honest
  precondition: the sibling repos must be present on disk (in CI, a job checks them
  out first), and federation is directional, so declare it on both sides for
  symmetric coverage.
- **The macrokit, the horizon.** In an organization where everyone installs their
  own microkit, a referent can aggregate every registry into one org-wide map that
  each microkit queries: the central inventory, as a network rather than a server.

Two guardrails keep that from betraying the premise:

1. **Git-native, no server.** Each microkit publishes its registry (plain markdown);
   the macrokit aggregates by pull. The moment it becomes a live central service, it
   is the opaque store this whole method argues against. The aggregation stays
   readable files.
2. **Opt-in, metadata only.** Aggregating an org's agent registries is a surface.
   Federation is opt-in per microkit, and a registry exposes agent metadata (who does
   what), never the code.

The peer layer ships. The macrokit is a direction, not a claim.
