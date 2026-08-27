# Install

One command, any OS, run inside the repo where you want your agents governed:

```bash
uvx microwave-method
```

Prerequisites: `git`, Python 3.10+ and `uv` (the Python package runner, installs
in one line). The tool itself is standard library only, no packages. Your coding
agent (Claude Code, the supported harness) does the rest. No `uv`? The shell
bootstrap below does the same by cloning the repo (the desktop icon is uvx-only).

Note on `python`: commands in the flows are written `python gates/...`. On
macOS/Linux where only `python3` exists, substitute it (or
`alias python=python3`); the pre-commit hook and CI resolve this
automatically.

## Windows (PowerShell 7+)

Download, read, then run. Piping a URL into `iex` executes whatever is on the
default branch at that second:

```powershell
cd your-repo
irm https://raw.githubusercontent.com/microphage-create/microwave-method/main/install/bootstrap.ps1 -OutFile bootstrap.ps1
# read it, then:
./bootstrap.ps1
```

The one-liner, if you accept that trade: `irm <same url> | iex`.

Target another folder: set `$env:MICROWAVE_TARGET = "C:\path\to\repo"` first.
Pin what gets cloned: `$env:MICROWAVE_REF = "<branch-or-tag>"` (default `main`).
If script execution is blocked: `Set-ExecutionPolicy -Scope Process Bypass`.

## macOS / Linux

Same rule: fetch it, read it, run it.

```bash
cd your-repo
curl -fsSL https://raw.githubusercontent.com/microphage-create/microwave-method/main/install/bootstrap.sh -o bootstrap.sh
# read it, then:
bash bootstrap.sh
```

The one-liner, if you accept that trade: `curl -fsSL <same url> | bash`.

Target another folder: append it, `bash bootstrap.sh /path/to/repo`.
Pin what gets cloned: `MICROWAVE_REF=<branch-or-tag> bash bootstrap.sh` (default
`main`, cloned at HEAD).
If `python3` is missing on macOS: `xcode-select --install` or `brew install python`.

`uvx microwave-method` (top of this page) is the canonical one-command install,
published on PyPI, and the one you can pin to an exact release
(`uvx microwave-method==0.1.23`). The shell bootstrap above is the no-`uv`
fallback; it clones the repo and runs the shell installer (`install.sh` /
`install.ps1`), which is non-interactive: it wires the hook directly (additive, backs up any existing
pre-commit). The `uvx` path asks before any side effect.

## What the installer does (additive, never overwrites)

1. Copies `flows/`, `templates/`, `techniques/`, `slop/`, `gates/`,
   `embodiment/`, `hooks/`, `harness/` into your repo and seeds `wiki/`.
2. Drops the session-start context (`CLAUDE.md`) and the agent-zero card
   (`wiki/agents/microwave.md`), so no session opens wired to nothing.
3. Wires the pre-commit hook (gates run on every committed agent card).
4. Drops the CI workflow (`.github/workflows/gates.yml`) and a `CODEOWNERS`
   placeholder.
5. On the `uvx` path, after your yes: offers to put a Microwave desktop icon
   (agent zero) on your machine, and prints the three hardening steps that
   cannot be shipped as files: your gatekeeper's handle in CODEOWNERS, adapting
   `harness/claude-settings.example.json` into your harness, and branch
   protection (command provided).

## The onboarding, end to end

```
1. install (one line above)
2. tell your agent:  "run the Microwave welcome flow"  (it runs adopt for you)
   → scans wherever your agents sleep (.claude/, prompts/, repos)
   → one inventory entry per artifact in wiki/_archive/
   → the shopping list: wiki/_archive/BACKLOG.md
3. prune the backlog (you decide: migrate / merge / keep-as-is / reshape / retire)
4. tell your agent:  "run the Microwave create-agent flow for the first
   backlog entry"
   → the archived entry is the elicitation input: cheapest creation there is
   → gates, embodiment (your agent gets its icon and terminal), activation
5. repeat at your own pace; create net-new agents the same way
```

From zero to "the Microwave icon is on my desktop, my whole estate is mapped,
and my first governed agent has its own icon too" is one install line plus two
sentences said to your coding agent.

## Try it in two minutes (no writes)

See exactly which files would be created, with nothing touched:

```bash
uvx microwave-method --dry-run
```

It prints the additive file list and exits. Existing files are never in it,
because the installer never overwrites.

## Uninstall

One command removes every Microwave file still matching exactly what it installed
(byte-identical for copied files; the generated `CODEOWNERS` and `wiki/INDEX.md`
are matched against the exact text it wrote). It never deletes a file you edited
or your own atoms, and it restores a backed-up pre-commit hook if it made one:

```bash
uvx microwave-method --uninstall
```

Embodied agents: run `python embodiment/embody.py <card> --remove` first to also
clean their desktop profiles. The wiki is yours: plain markdown, keep it.

What this install does not give you, and when to skip it: `docs/limits.md`.
