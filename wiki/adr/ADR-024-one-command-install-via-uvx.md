---
type: adr
id: ADR-024
title: One-command install via uvx; distribution follows the Python core
status: accepted
date: 2026-08-19
scope: meta
---

# ADR-024: One-command install via uvx; distribution follows the Python core

## Context

Adoption wants BMad's one-command experience (`npx bmad-method install`): type
one line anywhere and be carried into the flow. BMad is a Node project, so npx
fits it natively. Microwave is Python end to end (gates, docgen, trace,
embodiment, all stdlib, ADR-007). Forcing npx would make the user install Node
just to lay down a Python tool: a second runtime for nothing, and incoherent.

## Decision

Install is a single command, `uvx microwave-method` (the bare name "microwave"
is already taken on PyPI). `uv` is the Python equivalent of npx: it fetches and
runs the tool in an isolated environment, one syntax on every OS, no Node. The
package is self-contained: it embeds the framework files (the build force-
includes the repo-root dirs into the wheel), so it never reaches back to GitHub
and works even into a private repo. It has no runtime dependencies (stdlib only,
ADR-007); uv provides the environment.

One Python installer (`microwave_method/__init__.py`) becomes the canonical
path, a single cross-platform source; the shell installers (install.sh/.ps1)
stay only for the curl/irm bootstrap until it is repointed at the package. It
copies the files additively (never overwrites) and seeds the wiki: always safe.
Then, with a single confirmation (default yes), it sets up git if needed, wires
the pre-commit hook (backing up any existing one), and launches the detected
agent (claude) on "run the Microwave welcome flow". Decline, or run
non-interactively or with `MICROWAVE_NO_LAUNCH=1`, and it just prints that line:
no repo is created and no agent launched without a yes, so a stranger's first
run holds no surprise. The guided welcome itself is played by the agent
(ADR-023), because Microwave is a method, not a runtime.

The core stays Python. The value is zero-dependency: a gate that needs
`npm install` before it runs is a gate that does not run. Rewriting the core in
Node just to get a familiar install command is not worth redoing the whole
tool; instead distribution follows the core, never the reverse.

## Consequences

One command, one runtime for the user (Python, plus uv which installs in a
line). Honest limit: uv is less ubiquitous than npx, but Python is already the
sole prerequisite, so uv adds nothing foreign. Verified locally: `uvx --from .
microwave-method` builds the wheel and installs 52 files into a fresh repo, the
gates run there. Publishing to PyPI and making the repo public is the
irreversible step, gated on explicit go; until then the local build is the path.

## Links

[[ADR-007-stdlib-gates]] [[ADR-023-guided-flows-adapt-to-the-person]] [[ADR-010-adopt-first]]
