# Brief: Microwave Method core

The framework itself, as its own first product-plane project. Dogfood of
`templates/brief.md`.

## 1. Success criteria (verifiable)

- The gate pipeline runs green on this repository's own artifacts. Check:
  `python gates/run_gates.py wiki/agents/factory.md`
- A third party can install the method into a fresh repo without any context
  beyond the README. Check: run `install/install.sh <fresh-repo>` and execute
  `flows/create-agent.md` end to end
- The wiki index covers every atom. Check: `python gates/gate_wiki.py`

## 2. Volume cap

80 files. The initial cap of 30 was raised extension by extension, each one
requested by the owner in session (devil loop, adopt, bootstrap, technique
banks, anti-slop): the cap did its job as a checkpoint trigger. Anything
beyond (icon bank, docs site, extra adapters) waits for a human checkpoint.

## 3. Abort conditions

- Any file would need content from the author's private systems (client
  names, strategy, memory): stop, genericize, or drop.
- An adapter requires a non-stdlib dependency for its core path: stop and
  reconsider (ADR-007).
