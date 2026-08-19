# Flow: create-feature (Pass 2)

Light, every time. The agent is already contextualized by its card and its
project wiki: **no PRD**.

## Step 1: Load context

Read, in order: your agent card (`wiki/agents/<slug>.md`), the project wiki
index entries for this domain, the relevant ADRs and learnings. Start from
acquired knowledge, never from zero.

## Step 2: Story

Fill `templates/story.md`: intent in one sentence, then 3-8 done-criteria.
Each criterion MUST name an executable check (a test, a command, a measurable
assertion). `gate_testable` rejects hollow criteria.

## Step 3: Build

Build until every check passes. Do not close a story with a red check: the
contract is in the checks, not on paper.

## Step 4: Trace

Before closing:
- New decision made? → `templates/adr.md` into the project wiki.
- Something learned the hard way? → `templates/learning.md`.
- Bug found and fixed? → `templates/bug.md` (root cause + fix + test).
- Update `wiki/INDEX.md` (one line per new atom).

Run `python gates/gate_wiki.py` to verify links and index coverage, and
`python gates/gate_slop.py` on what you wrote: durable artifacts do not
ship with LLM tells (`slop/slop-rules.csv`; your org may have added rows).
When fixing a hit, rewrite the sentence: character-swapping a banned marker
is itself slop.

## Improvement variant

Improving an existing feature: same flow, but step 1 includes reading the
feature's past stories and bugs. Expect the story to be shorter: that is the
compounding working.
