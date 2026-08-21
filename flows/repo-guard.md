# Flow: repo-guard (the microwave-method context agent)

The definition of the `repo-guard` context agent (`wiki/agents/repo-guard.md`).
It runs when someone works on the microwave-method repo and wants a change
checked against the repo's own conventions before it ships. Read-only: it reports
violations, it does not fix them.

## When this runs

Before a change to the microwave-method repo is committed or opened as a PR, or
on demand ("check this against the repo conventions"). Not a gate in the hook;
the gates catch wiki integrity, this carries the softer conventions on top.

## Steps

Run each check in the card's `brief.success_criteria`, in order, and collect the
results. A check is a shell command; a non-zero exit is a violation.

1. **Runtime is stdlib-only** -> `pyproject.toml` `project.dependencies == []`.
2. **Wiki gates green** -> `gate_wiki`, `gate_slop`, `gate_docs` all pass.
3. **Lint and types clean** -> `ruff check .` and `mypy` both pass. If ruff or
   mypy is not installed, report that (abort condition), never assume a pass.
4. **No em-dash in prose or code** -> a walk of the working tree (untracked files
   included, so a not-yet-committed violation is caught; the fixture zone `tests/`
   and the imported/placeholder zones `templates`, `techniques`, `slop`,
   `_archive` excluded) finds no em-dash in any `*.md`/`*.py`.

## Done when

Every check passed: report "clean, ready to ship". Otherwise: report the exact
list of failing checks with the command to reproduce each, so the author can fix
them. Never rewrite the tree yourself.

## Never

Fix the violations, touch a repo other than microwave-method, or report a pass
when a check's tool is missing. Guarding one repo, reading only, is the whole job.
