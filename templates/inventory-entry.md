---
type: inventory-entry
name: found artifact name
provenance: path/or/url/where/it/was/found
kind: agent | skill | command | prompt | workflow | unknown
form: agent | data-source | tool | doctrine | unknown  # ADR-015: what it IS, not what it was filed as
apparent_mission: one sentence, inferred, marked as inferred
apparent_blast_radius: read | write | spend | prod | unknown
last_touched: YYYY-MM-DD or unknown
referenced_by: [what else points at it, or none found]
disposition: pending
scanned: YYYY-MM-DD
---

# {name}

## What it appears to do

Inferred from the artifact itself; quote its own text where possible. Record
what IS, not what should be.

## Notes for migration

Anything the pass-1 elicitation should know: hardcoded paths, secrets
handling, overlaps noticed with other entries, obvious rot.
