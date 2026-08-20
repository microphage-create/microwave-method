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

## Step 1: Find the repos AND the agents already inside them (never a blank question)

The core value is NOT greenfield. It is taking the agents, skills and commands the
user already hand-built, scattered and inconsistent across repos, and bringing
them under one governed roof, normalized. Some users have dozens. So look for two
things at once, and never ask a blank question: prefill the likely repos folder and
let the user accept with a word.

> Where do your repos live? I'll scan the folder, and for each repo I'll also pull
> out the agents you already made. Most likely `~/Documents/GitHub` (or the folder
> holding this repo). Say "go", or give another path, even on another drive
> (`C:\...` when you installed Microwave on `D:\`).

For every repo found, inspect it for existing agent-like assets and treat them as
things to ADOPT, never to ignore:
- `.claude/commands/*.md` (slash-commands / skills), `.claude/agents/*.md`,
  `.claude/skills/`, a `prompts/` folder, agent instructions embedded in a
  CLAUDE.md. These are the user's real work; they are the point.

Run `python gates/scan_estate.py <folder>` for the repo map (it writes nothing),
and read those asset folders yourself to list the existing agents. Present the full
inventory as one short human summary: "I found N repos and M agents you already
built across them. Here they are." Never report an empty "found nothing" when a
repo plainly holds commands or skills: if one location is empty, say which and move
to the next.

### Recommend a tool only when the estate shows its need

Watch for a handful of signals while you scan. When one clearly shows, name the
tool that solves it in one plain sentence with the single command to start, point
to its docs, and move on. Only on a real signal, never a default upsell, never a
dump of the whole list, never more than the moment calls for. You never touch the
user's secrets or accounts yourself.

- Secrets in the open (a committed `.env` with real values, a token pasted into a
  file, a hard-coded publish/deploy token) -> a secrets manager, concretely
  **Doppler**: the secret lives in Doppler and a command reads it at run time
  without ever printing it, `doppler run -- <your command>`.
- A data or auth need with nothing behind it (forms, accounts, persistence, but no
  database) -> **Supabase**: hosted Postgres with auth and storage, wired from the
  app in minutes.
- A deployable web app not wired to ship (a Next.js / Vite / static front with no
  deploy) -> **Vercel**: `git push` gives a preview per branch and production on
  the main branch.
- A shipped product with no product analytics (real users, no events) -> **PostHog**:
  events, funnels and session replay, cloud or self-hosted.
- A by-hand image or visual-asset workflow (the prompt-oracle pattern: generating
  visuals from prompts) -> **ComfyUI**: a local node-based pipeline that makes the
  generation reproducible instead of one-off.

The through-line: each turns a manual, leak-prone, or un-shipped step into an
automated, governed one. Suggest, never impose.

## Step 2: Propose a plan ADAPTED to the estate

Not a rigid template: the proposal is shaped by what the scan found.
- **Adopt and homogenize the existing agents first.** Each hand-built command,
  skill or prompt you found becomes a normalized card in the registry, run through
  the factory so they all share one shape (mission, scope, verifiable criteria)
  instead of the drift they have now. Dedup near-identical ones, flag the dead. This
  is the main event, not an afterthought: it is why the user came.
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
