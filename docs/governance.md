# Governance

Four rules. Each states plainly whether a machine enforces it or the flows merely
encourage it: overclaiming enforcement is the fastest way to lose trust.

## 1. Subsidiarity

Every atom lives at the lowest level that suffices. Promotion from project wiki
to meta wiki happens only through the gatekeeper. Purges are traced.

## 2. The meta plane governs creators, not creations

No committee reviews every feature (that is the curation bottleneck that kills
knowledge systems). The meta plane imposes the gates; the product plane runs
them locally. The human gatekeeper only sees what moves up, and full-path
activations.

## 3. The factory is the single entry point of creation

Agents may create agents, only through the factory. Out-of-band creation is
discouraged by the flows and the write-deny rules, and caught at the commit
boundary by the gates, CODEOWNERS and branch protection on the protected space.
It is a governed convention with real teeth where it counts, not a runtime that
intercepts every keystroke. This is the anti-sprawl invariant.

## 4. Staged gatekeepers

One human gatekeeper at the top (meta wiki). Delegated gatekeepers per
domain (project wikis). Volume caps per cycle and purge-of-the-unconsulted
everywhere, so the gatekeeper is never the bottleneck.

## Gates, not meetings

The pipeline (`gates/run_gates.py`) is a CI for agent creation:

`gate_antidup → gate_brief → gate_schema → gate_testable → gate_embodiment → gate_slop → gate_wiki`

Each gate exits non-zero with an actionable message. Fix, re-run. One human
point: the gatekeeper, full path only.

**Known failure mode: gate gaming.** A creator (human or agent) can write
trivial done-criteria just to pass `gate_testable`, which checks that each
criterion NAMES a check, not that the check exists or ran. Gates check form,
not whether the work was actually done. Three answers, layered: the **devil review**
(`flows/devil-review.md`, orchestrated by `flows/devil-loop.md`) attacks
substance with fresh eyes before any full-path judgment; the full path keeps
its single human; and everything is traced in the wiki, so pertinence is
judged after the fact on traces, and an agent whose criteria prove hollow
gets purged. The loop closes itself.

## Enforcement: structural vs cooperative

Which is which, plainly. Overclaiming here is how you lose a security-minded
reader.

**Structural (a machine refuses):**
- **Commit gate**: the pre-commit hook and CI run the gates and block a commit
  that fails. Shipped: `hooks/pre-commit` + installers, `.github/workflows/gates.yml`.
- **Protected space**: `CODEOWNERS` + branch protection require a gatekeeper's
  merge for `gates/`, `hooks/`, CI, `CODEOWNERS`, and the main wiki spaces. You
  enable branch protection (required check `gates`, `enforce_admins`); the
  installer prints the `gh` command. Without it, this floor is advisory.

**Cooperative (the harness or agent must play along):**
- **Deny-rules** (`harness/claude-settings.example.json`) deny the agent's Read
  and Write TOOLS on secrets and protected paths. They are an example, Claude-
  Code-specific, and do NOT cover the shell: a determined agent can still `cat`
  a file. Treat them as a hint that keeps an honest agent on-path, never as a
  sandbox or as secret protection. The real protection for a secret is not to
  keep it in the repo (env vars, a secret manager).
- **The flows, the devil pass, the gatekeeper's judgment**: conventions the
  method encourages. They are how substance is reviewed, not machine-guaranteed.

## Constitution, not dogma

Inviolable in execution, amendable only through process. Nobody bypasses a
rule; anybody may propose to change one, through the single path:
`flows/amend-rule.md` (ADR in the meta wiki + gatekeeper judgment + PR on the
protected space). A rule frozen forever pushes people to desert the system
(out-of-band creation, the sprawl we fight); a rule you can bypass is not a
rule. For true emergencies: a traced break-glass with a mandatory post-mortem,
never a silent bypass. The rule for changing rules is itself gated.
