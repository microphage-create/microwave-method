# Flow: amend-rule (the constitution)

Rules are inviolable in execution and amendable only through this flow.
Nobody bypasses a rule; anybody may propose to change one.

## Path

1. **Write the amendment as an ADR** (`templates/adr.md`) in
   `wiki/_staging/`: which rule, what change, why the current rule fails
   (cite occurrences: an amendment without observed cost is rejected), what
   the new rule refuses and allows.
2. **Run the gates** on the ADR: `gate_wiki` (validates the adr type contract) and `gate_slop`.
3. **Gatekeeper judgment.** The gatekeeper (a human; see CODEOWNERS on
   `gates/`) accepts or rejects, in writing, in the ADR.
4. **Apply through a PR** touching the protected space (`gates/`, hooks,
   permission files). Required checks + CODEOWNERS make it impossible to merge
   without the gatekeeper: the rule for changing rules is itself gated.
5. **Distill** the decision into one actionable line in `wiki/RULES.md`
   (the live rule base) and set the ADR `status: distilled`. The ADR stays
   in `wiki/adr/` as archived rationale (NOT indexed per-line in
   wiki/INDEX.md, gate_wiki exempts it); RULES.md and the code are what
   govern. A rule enforced by a gate needs no living document beyond its
   line.

## Break-glass (true emergencies only)

If a rule blocks a genuine emergency: perform the minimal action, **trace it
immediately** (an ADR marked `break-glass` with what was done and why), and
run a post-mortem at the next session. A silent bypass is a firing offense for
an agent (purge) and a broken invariant for a human. Break-glass without a
post-mortem counts as a silent bypass.
