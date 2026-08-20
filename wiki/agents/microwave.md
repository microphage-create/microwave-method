---
type: agent-card
kind: service
name: Microwave
slug: microwave
status: active
blast_radius: read
mission: The factory's front door. Opens a context-loaded terminal on this repo and points you at the welcome and create-agent flows, so no session starts wired to nothing.
inputs: [the repo, wiki INDEX, agent registry]
outputs: [a contextualized session in this repo]
definition_path: flows/welcome.md
owner: "@microphage-create"
synonyms: [agent zero, alpha, front door, entry point, launcher, the microwave]
anti_dup_rationale: "No other card is the entry point. The factory creates agents, the gatekeeper judges, the librarian curates; none of them is the desktop door a person double-clicks to land in a repo that already knows itself. This is agent zero: it creates nothing and judges nothing, it only opens a session that is already contextualized."
created_in_minutes: 0
embodiment:
  display_name: Microwave
  icon: embodiment/icons/microwave.png
  palette:
    bg: "#475559"
    fg: "#E8EEEE"
    accent: "#7FB0B0"
  launch: claude
  embodied: false
brief:
  success_criteria:
    - criterion: Double-clicking its desktop icon opens a terminal already cd'd into the repo
      check: the Windows Terminal profile commandline contains cd '<repo>' and the .lnk targets wt.exe -p "Microwave"
    - criterion: The opened session is contextualized, not blank
      check: the repo carries a CLAUDE.md that tells the agent to load the registry and wiki index on start
  volume_cap: "1 agent-zero icon per install; the factory's own agents get theirs through embody.py"
  abort_conditions:
    - The target has no Windows Terminal / no Desktop and no GUI launcher can be written (fall back to the printed start line)
    - settings.json cannot be parsed or backed up (never edit a harness config you cannot restore)
---

# Microwave (agent zero)

## Mission

Microwave is the front door of its own factory. Installing the method drops one
icon on the desktop; double-clicking it opens a terminal already sitting in the
repo, with the registry and wiki one command away. From there the person runs
the welcome flow, then the create-agent flow, and every agent they build gets
its own icon the same way. Agent zero is how a blank machine becomes a desk of
governed agents.

## Scope

**In**: opening a contextualized session (terminal cd'd into the repo, CLAUDE.md
loaded), pointing at `flows/welcome.md`.
**Out**: creating agents (the factory only), judging them (the gatekeeper only),
writing to the wiki (it is read-only; the session it opens may write, under the
same gates as everyone else).

## Embodiment

The Windows adapter writes a Windows Terminal profile + colorScheme and a
desktop `.lnk`; macOS gets an iTerm2 profile + `.app`; Linux a `.desktop` entry.
The icon is the Microphage M on petrol, the constant of the product family: the
same M, a different name per product.
