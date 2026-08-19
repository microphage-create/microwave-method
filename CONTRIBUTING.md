# Contributing

The most valuable first contribution takes five minutes: run the macOS or
Linux embodiment adapter on a real machine and report what happened (see
`docs/embodiment.md`). Open an issue titled `adapter-report: <os>` with your
OS version, your terminal, and the output of:

```
python3 embodiment/embody.py wiki/agents/factory.md --dry-run
python3 embodiment/embody.py wiki/agents/factory.md
python3 embodiment/embody.py wiki/agents/factory.md --remove
```

## Pull requests

- Run the gates before pushing: `python gates/gate_wiki.py && python
  gates/gate_slop.py` (the pre-commit hook does this if you ran
  `hooks/install-hooks.sh`). CI runs them on every PR.
- Changes to `gates/`, `flows/`, `hooks/`, `harness/` or `wiki/adr/` go
  through the amend-rule flow (`flows/amend-rule.md`) and require gatekeeper
  review (see CODEOWNERS).
- Keep it stdlib-only (ADR-007): a PR adding a dependency to a gate or an
  adapter core path will be declined.
- Prose follows the repo's own slop rules (`slop/slop-rules.csv`); the gates
  will tell you.

## Scope

Bug fixes, adapter reports, portability fixes and slop-rule contributions
are welcome directly. New flows, gates or adapters: open an issue first so
the design discussion happens before the code.
