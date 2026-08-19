# Governance

Four rules, all structural. Installed, not preached.

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
refused at execution time (blocking hook), not discouraged in a wiki page.
This is the anti-sprawl invariant, and what makes recursion safe.

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
trivial done-criteria just to pass `gate_testable`. Gates check existence and
execution, not pertinence. Three answers, layered: the **devil review**
(`flows/devil-review.md`, orchestrated by `flows/devil-loop.md`) attacks
substance with fresh eyes before any full-path judgment; the full path keeps
its single human; and everything is traced in the wiki, so pertinence is
judged after the fact on traces, and an agent whose criteria prove hollow
gets purged. The loop closes itself.

## Harness-level enforcement

Rules are not prompt instructions. They live in the execution layer, the same
way a coding agent is denied reading your `.env` by permission rules: the
harness refuses, goodwill is not involved. Three structural floors:

1. **Permissions / deny rules**: the agent CANNOT read secrets, write to the
   main wiki spaces directly, or modify the gates. Shipped:
   `harness/claude-settings.example.json` (adapt to your harness).
2. **Blocking hooks**: gates run on every staged card at commit time.
   Shipped: `hooks/pre-commit` + installers (`hooks/install-hooks.sh|.ps1`),
   wired automatically by `install/`.
3. **Repo layer**: required CI checks + CODEOWNERS on the protected space.
   Shipped: `.github/workflows/gates.yml` and `CODEOWNERS`. One setting
   cannot be shipped as a file: **branch protection** (required check
   `gates`, `enforce_admins`) must be enabled on your host: the installer
   prints the `gh` command. With it on, a human cannot merge red, admin
   included; without it, floor 3 is advisory.

## Constitution, not dogma

Inviolable in execution, amendable only through process. Nobody bypasses a
rule; anybody may propose to change one, through the single path:
`flows/amend-rule.md` (ADR in the meta wiki + gatekeeper judgment + PR on the
protected space). A rule frozen forever pushes people to desert the system
(out-of-band creation, the sprawl we fight); a rule you can bypass is not a
rule. For true emergencies: a traced break-glass with a mandatory post-mortem,
never a silent bypass. The rule for changing rules is itself gated.
