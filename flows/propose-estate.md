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
