# Developing Microwave

The shipped tool is stdlib-only (ADR-007). These are DEV tools: they check the
framework's own code and never become runtime dependencies. Run them with `uvx`
so nothing is installed globally.

## The checks (what CI runs)

Two workflows. `gates.yml` is what the installers ship to an adopter (a single
gate on their governed repo). `ci.yml` is Microwave's own bar and is NOT shipped.

| Check | Command | What it guards |
|---|---|---|
| Lint | `uvx ruff@0.16.4 check .` | pyflakes, bugbear, imports, pyupgrade (config: `[tool.ruff]`) |
| Typecheck | `uvx mypy@2.3.1` | the gates, embodiment, installer (config: `[tool.mypy]`) |
| Spellcheck | `uvx codespell@2.4.3` | typos in the prose-heavy wiki + code (`[tool.codespell]`) |
| Tests | `python -m unittest discover tests` | the suite; stdlib-only-runnable |
| Property layer | `uvx --with hypothesis python -m unittest discover tests` | parser robustness (skips if hypothesis is absent) |
| Gates on the wiki | `python gates/gate_wiki.py` (and `gate_slop.py`, `gate_docs.py`) | the estate's own integrity |

## Two rules learned the hard way

- **Verify under the CI platform, not just your host.** `ci.yml` runs mypy +
  tests across {ubuntu, windows, macos} x {3.10, 3.11, 3.12, 3.13}, because a
  Windows-only green run once merged a Linux-red change (`ctypes.windll` is
  win32-only). If you touch platform-specific code, run `uvx mypy@2.3.1
  --platform linux` before you push.
- **Pin the linters.** ruff/mypy/codespell are pinned in `ci.yml`, so a new
  default rule in a future release can't redden code nobody touched.

## Where the tooling was borrowed from

The static-analysis stack, the version matrix, the spellchecker, and the
property tests were adopted from well-engineered open-source estates (opensre,
httpx, pydantic, rich): the framework improves itself by taking the best
practice it finds and coming back stronger (see `docs/self-improvement.md`).
