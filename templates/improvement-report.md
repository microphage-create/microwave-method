---
type: improvement-report
id: IR-000
title: short shape of the problem, no estate data
kind: bug | friction | idea
surface: gate | flow | hook | embodiment | adopt | docs | other
severity: blocks | slows | polish
status: open | shipped | declined
scrubbed: true
date: YYYY-MM-DD
source_signal: dogfood | network | maintainer
---

# IR-000: {title}

## The shape

What broke or grated, described as a PATTERN, not an instance. Right:
"gate_embodiment crashed on a staged card copied into a tmp dir with no repo
above it." Wrong: anything naming the estate's agents, paths, missions, or
content. If you cannot state it without the estate's data, it is not ready to
leave the machine.

## Reproduce

The smallest sequence that triggers it, in framework terms only.

## Fix or idea

The proposed change, or the open question if not yet known.

## Ship

Branch, PR, and the mode that closed it (semi-auto human-merge, or full-auto
with the scope reason). Filled as the cycle completes.

<!--
Scrubbing rule (ADR-029): this file may be shared upstream only if `scrubbed`
is true AND it carries no agent name, path, mission, or content from the estate
it was found on. The shape of a problem travels; the data never does.
-->
