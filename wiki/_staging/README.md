# Staging

Candidates awaiting judgment: draft agent cards (from pass 1) and atoms
proposed for promotion to the meta plane.

Rules:
- Nothing moves from here to `wiki/agents/` or `wiki/adr/` except through the
  gatekeeper (full path) or green gates (fast path, cards with
  `blast_radius: read` only).
- **A candidate committed to git is gate-green.** Work-in-progress stays in
  your working tree; the pre-commit hook enforces this. Red cards do not
  enter history: what the team can check out is always a valid state.
- Kills are traced: a rejected candidate stays here with `status: rejected`
  and a rationale, until periodically archived.
- Staging is not storage: anything older than the review cycle is a red flag
  (promote or purge).
