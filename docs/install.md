# Install

One command, any OS, run inside the repo where you want your agents governed:

```bash
uvx microwave-method
```

Prerequisites: `git`, Python 3.10+ and `uv` (the Python package runner, installs
in one line). The tool itself is standard library only, no packages. Your coding
agent (Claude Code, Codex, Cursor, ...) does the rest. No `uv`? The shell
bootstrap below does the same by cloning the repo.

Note on `python`: commands in the flows are written `python gates/...`. On
macOS/Linux where only `python3` exists, substitute it (or
`alias python=python3`); the pre-commit hook and CI resolve this
automatically.

## Windows (PowerShell 7+)

```powershell
cd your-repo
irm https://raw.githubusercontent.com/microphage-create/microwave-method/main/install/bootstrap.ps1 | iex
```

Target another folder: set `$env:MICROWAVE_TARGET = "C:\path\to\repo"` first.
If script execution is blocked: `Set-ExecutionPolicy -Scope Process Bypass`.

## macOS / Linux

```bash
cd your-repo
curl -fsSL https://raw.githubusercontent.com/microphage-create/microwave-method/main/install/bootstrap.sh | bash
```

Target another folder: append it, `... | bash -s -- /path/to/repo`.
If `python3` is missing on macOS: `xcode-select --install` or `brew install python`.

`uvx microwave-method` (top of this page) is the canonical one-command install,
published on PyPI. The shell bootstrap above is the no-`uv` fallback; it clones
the repo and runs the same Python installer.

## What the installer does (additive, never overwrites)

1. Copies `flows/`, `templates/`, `techniques/`, `slop/`, `gates/`,
   `embodiment/`, `hooks/`, `harness/` into your repo and seeds `wiki/`.
2. Wires the pre-commit hook (gates run on every committed agent card).
3. Drops the CI workflow (`.github/workflows/gates.yml`) and a `CODEOWNERS`
   placeholder.
4. Prints the two hardening steps that cannot be shipped as files: your
   gatekeeper's handle in CODEOWNERS, and branch protection (command
   provided).

## The onboarding, end to end

```
1. install (one line above)
2. tell your agent:  "run the Microwave adopt flow"
   → scans wherever your agents sleep (.claude/, prompts/, repos)
   → one inventory entry per artifact in wiki/_archive/
   → the shopping list: wiki/_archive/BACKLOG.md
3. prune the backlog (you decide: migrate / merge / keep-as-is / retire)
4. tell your agent:  "run the Microwave create-agent flow for the first
   backlog entry"
   → the archived entry is the elicitation input: cheapest creation there is
   → gates, embodiment (your agent gets its icon and terminal), activation
5. repeat at your own pace; create net-new agents the same way
```

From zero to "my whole estate is mapped and my first governed agent has an
icon on my desktop" is one install line plus two sentences said to your
coding agent.

## Uninstall

Remove the copied directories and `.git/hooks/pre-commit`. Embodied agents:
`python embodiment/embody.py <card> --remove` cleans profiles and launchers.
The wiki is yours: plain markdown, keep it.
