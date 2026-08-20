# Flow: propose-estate (scan the user's repos, propose a context/service map)

This is the take-by-the-hand onboarding from the user's OWN estate, not a blank
page. You, the coding agent, drive it; the user answers simple questions and says
yes. It scans a folder of repos, proposes an architecture adapted to what is
actually there, then creates it one agent at a time through the factory. It does
not re-implement creation: it orchestrates `scan_estate.py` and `create-agent.md`.

## The one rule

Fluidity above everything. One action at a time, never a blank prompt. After each
step, say what just happened in one plain sentence, then propose the next with a
default the user can accept by just agreeing. Always offer a clean stop.

## Step 1: Scan everything

Ask, prefilled with a guess from what you can see (the parent of the current
folder is usually the repos directory):

> Where do your repos live? (e.g. `~/Documents/GitHub`)

Run `python gates/scan_estate.py <that folder>`. It writes nothing. Present the
result as a short human summary, not the raw output: "I found N repos. Here they
are with the stack I detected."

### While you scan: one hygiene nudge, never a lecture

If the scan surfaces secrets living in the open (a committed `.env` holding real
values, an API key or token pasted into a file, a hard-coded publish/deploy
token), mention it once, in one plain sentence, and recommend a secrets manager
so nothing leaks and nothing has to be pasted by hand again. Doppler is the
concrete suggestion: a secret lives in `Doppler`, and a command reads it at run
time without ever printing it, e.g. `doppler run -- <your command>` for a deploy
or publish. Give the one line, point to their docs, and move on. Never block the
scan on it, never nag, never touch their secrets yourself: it is a suggestion the
user takes or leaves. Recommend a tool only when the estate actually shows the
problem it solves, not as a default upsell.

## Step 2: Propose a plan ADAPTED to the estate

Not a rigid template: the proposal is shaped by what the scan found.
- One **context** agent per repo (the guard that carries that repo's conventions),
  its `repo:` set, its stack hint carried into the mission.
- The transversal **services** to create once and share (`code-review`,
  `copywriter`, ...), trimmed to what these repos plausibly need.
- Skip repos that already carry Microwave (the scan flags them); offer to refresh
  instead of recreate.
Show the map, let the user prune it: migrate / merge / skip / reshape, their call.

## Step 3: Apply, one at a time

For each approved item, run `flows/create-agent.md`:
- a repo guard -> `kind: context`, `repo:` set, `uses:` listing the services it
  wires (each must resolve, `gate_uses` checks it);
- a shared tool -> `kind: service`, no repo.
Ask before every write. Never create in bulk behind the user's back.

## Step 3b: Questions and brainstorm when it is fuzzy

If a repo's purpose or a service's shape is unclear, do NOT guess: escalate to
elicitation, and to the brainstorm bank (`techniques/`) when the intent is really
fuzzy. A context agent built on a wrong guess is worse than one more question.

## Step 4: Await the result

Each creation runs its gates, gets its embodiment (icon + terminal), and is
activated. Report what was created in one plain sentence per agent, and where the
map now stands: "You now have N repo guards and M shared services, all in the
registry." Offer to continue or stop.
