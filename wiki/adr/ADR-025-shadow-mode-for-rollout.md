---
type: adr
id: ADR-025
title: Shadow mode so gates roll out with a grace period, not a wall
status: accepted
date: 2026-08-20
scope: meta
---

# ADR-025: Shadow mode so gates roll out with a grace period, not a wall

## Context

The one adoption failure a governed method has to survive: a team installs it,
the gates run strict on day one, and the first Friday-night hotfix hits a red CI.
People reach for `--no-verify`, disable the hook, and within weeks the discipline
is off. This is the objection that actually lands against enforced discipline, and
it is cultural, not technical.

## Decision

Ship a shadow mode. `MICROWAVE_SHADOW=1` makes every gate report what it WOULD
block (`SHADOW: would block: ...`) and exit 0 instead of non-zero. A repo runs
shadow for its first days so the team learns the rules against real commits, then
unsets it to enforce. It is honored in one place, `_lib.fail()`, so every gate
obeys the single switch.

## Consequences

Easier: adoption without a wall; the discipline arrives with a grace period.
Harder: a team can leave shadow on forever and get no enforcement. That is a
social risk, not a technical one: branch protection with the strict `gates` check
is the backstop a repo owner controls, and it is unaffected by a contributor's
local shadow flag. Strict stays the default; shadow is opt-in and loud.

## Links

[[ADR-006-harness-enforcement]]
