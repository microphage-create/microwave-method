---
type: agent-card
# kind: context guards one repo (also set repo:); service is transversal (no repo)
kind: service
name: Example Agent
slug: example-agent
# when kind is context, set the repo this agent guards (uncomment, keep it clean):
# repo: my-repo
status: staging
blast_radius: read
mission: One sentence stating what this agent does and for whom.
inputs: [what it consumes]
outputs: [what it produces]
definition_path: path/to/the/agent/definition
owner: "@your-gatekeeper"
synonyms: [alternative, words, for, anti-dup, search]
# transversal services this agent calls; each must resolve (gate_uses):
# uses: [service-slug]
anti_dup_rationale: ""
created_in_minutes: 0
# embodiment: REQUIRED only for write/spend/prod agents (a read-only agent
#   may omit this whole block, ADR-003 amended). For a powerful agent,
#   uncomment and fill it; the human validates the icon.
# embodiment:
#   display_name: Example
#   icon: embodiment/icons/example.png
#   palette: { bg: "#14181a", fg: "#e6ebeb", accent: "#9db8bd" }
#   embodied: false
#   launch: optional bare command; shell metacharacters are rejected
brief:
  success_criteria:
    - criterion: The agent accomplishes X measurably
      check: command or executable assertion proving it
  volume_cap: "N items max before human checkpoint"
  abort_conditions:
    - situation where the agent MUST stop and escalate
---

# Example Agent

## Mission

One short paragraph. Who uses it, for what, when it applies.

## Scope

**In**: what it handles.
**Out**: what it explicitly refuses (out-of-scope is a feature).

## Interfaces

What it reads, what it writes, which other agents it may call (registry slugs
only: calls are discovered through the index, never hardcoded).

## Notes

Anything the next reader (human or LLM) needs that the fields above cannot
carry.
