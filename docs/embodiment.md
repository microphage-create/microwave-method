# Embodiment: agents as apps

An agent that can do damage (write/spend/prod) is not done until it has a
body; a read-only agent may stay bodiless (ADR-003 amended). For a powerful
agent, pass 1 generates a physical
desktop presence for the agent: an icon, a short name, a themed terminal
profile, a launcher. This is a **mandatory, blocking step** of the creation
flow (`gate_embodiment`).

## Why a body

Adoption is the documented graveyard of every knowledge system: catalogs die in
six months; NASA's much-studied lessons-learned system went largely unused by
its intended audience. An agent you can see and launch like an app gets used; an agent invoked
by a memorized command dies. Visual identity means zero cognitive load, and
with five terminals open in parallel, each session is identifiable at a glance
by its color and logo.

## Terminals dressed as apps

These are **not GUI apps replacing the terminal**. The launcher opens a
dedicated terminal profile (own colors, own icon, own name) that loads the
agent's context. Full terminal power stays; only its anonymity goes.

## One manifest, N adapters

The identity lives in the agent card (embodiment block): short name, slug, one
source PNG icon, a palette (bg / fg / accent). Each OS adapter compiles that
manifest into native artifacts. Never three parallel scripts to maintain.

| OS | Artifacts | Status |
|---|---|---|
| Windows | Windows Terminal profile + color scheme in `settings.json`, `.lnk` on the desktop pointing to `wt.exe -p "<name>"`, `.ico`; timestamped backup before any edit | **tested** (reference adapter) |
| macOS | iTerm2 Dynamic Profile (JSON dropped in `DynamicProfiles/`, additive) + Terminal.app fallback via a `.command` file; launcher = minimal `.app` bundle with `.icns` | **experimental: written, not yet run on a Mac. Reports and PRs welcome.** |
| Linux | `.desktop` entry (`~/.local/share/applications` + desktop, PNG icon); terminals: Kitty, WezTerm, GNOME Terminal; generic fallback `$TERMINAL` | **experimental: written, not yet run on Linux. Reports and PRs welcome.** |

Testing an experimental adapter takes five minutes: run
`python3 embodiment/embody.py <card> --dry-run`, then for real, then
`--remove`. Open an issue with what happened: that is the whole
contribution.

Icon: one source PNG per agent, converted automatically (`.ico`, `.icns`, PNG).

Common rules: back up any edited config before writing, additive operations by
default, clean uninstall (an adapter knows how to remove what it added).

## Usage

```
python embodiment/embody.py <agent-card.md> [--os windows|macos|linux] [--dry-run]
python embodiment/embody.py <agent-card.md> --remove
```

The adapter reads the embodiment block of the card, generates the artifacts,
and writes back the `embodied: true` flag that `gate_embodiment` checks.
