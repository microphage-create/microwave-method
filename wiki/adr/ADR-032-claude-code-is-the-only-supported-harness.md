---
type: adr
id: ADR-032
title: Claude Code is the only supported harness
status: accepted
date: 2026-08-27
scope: meta
author: "@microphage-create"
---

# ADR-032: Claude Code is the only supported harness

## Context

The repo advertised three harnesses (Claude Code, Codex, Cursor) and shipped
`AGENTS.md` alongside `CLAUDE.md` so the other two would find their session-start
context. Only one of the three was ever run: every flow, every deny-rule example
and every dogfooding session happened in Claude Code. The other two were a claim
with no test behind it, and `docs/limits.md` had to say so, which is the shape of
a promise that costs more than it returns. Supporting a harness means running its
sessions, watching where the flows break in it, and keeping a context file
correct for it. Nobody was doing that for two of the three.

## Decision

Claude Code is the supported harness. One context file ships, `CLAUDE.md`, and
`AGENTS.md` is removed from the repo and from what the installers drop. The docs
name Claude Code where they used to list three tools, and the deny-rules example
(`harness/claude-settings.example.json`) is stated as the harness integration
rather than as one adapter among several.

This narrows what is claimed, not what is possible: the gates are
standard-library Python that anything can shell out to, and the flows are plain
markdown. An adopter on another harness writes their own context file and points
it at the same flows. That is a port, unsupported and untested, not a feature.

## Consequences

Easier: one harness to run the flows in, one context file to keep correct, one
deny-rule surface that actually corresponds to a tool. The honesty section of
`docs/limits.md` loses a caveat instead of carrying it.

Harder: an adopter on Codex or Cursor gets nothing pre-wired and has to write the
context file, which is the cost of not pretending. Installs that predate this ADR
carry an `AGENTS.md` Microwave no longer ships, so `--uninstall` keeps a copy of
the text it used to write and removes the file only when it still matches, the
same rule that governs every other uninstalled file. Reversible: adding a harness
back means shipping its context file, its deny-rule equivalent, and a session
that proves a creation flow completes in it. Until those three exist, the repo
says Claude Code.

## Links

[[ADR-006-harness-enforcement]] [[ADR-007-stdlib-gates]] [[ADR-024-one-command-install-via-uvx]]
