#Requires -Version 7
# Microwave Method installer (Windows, PowerShell 7+)
# Copies flows, templates, techniques, slop rules, gates and embodiment
# tooling into a target repo and seeds the wiki. Additive: never overwrites
# existing files (the hook installer backs up an existing pre-commit).
param(
    [Parameter(Mandatory = $true)][string]$Target
)

$ErrorActionPreference = "Stop"
$src = Split-Path -Parent $PSScriptRoot
$dst = Resolve-Path $Target

git -C $dst rev-parse --is-inside-work-tree *> $null
$isRepo = ($LASTEXITCODE -eq 0)
if (-not $isRepo) {
    Write-Host "warning: $dst is not a git repository yet. Run 'git init' here first, so the gates can guard the repo." -ForegroundColor Yellow
}

$dirs = @("flows", "templates", "techniques", "slop", "gates", "embodiment", "hooks", "harness", ".claude/commands")
foreach ($d in $dirs) {
    $from = Join-Path $src $d
    $to = Join-Path $dst $d
    New-Item -ItemType Directory -Force -Path $to | Out-Null
    Get-ChildItem -Recurse -File $from | Where-Object { $_.FullName -notmatch '[\\/](icons|__pycache__)[\\/]' -and $_.Extension -ne '.pyc' } | ForEach-Object {
        $rel = $_.FullName.Substring($from.Length + 1)
        $out = Join-Path $to $rel
        if (-not (Test-Path $out)) {
            New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
            Copy-Item $_.FullName $out
        }
    }
}

# CI + CODEOWNERS (placeholder to edit) + git hook wiring
New-Item -ItemType Directory -Force -Path (Join-Path $dst ".github/workflows") | Out-Null
$ci = Join-Path $dst ".github/workflows/gates.yml"
if (-not (Test-Path $ci)) { Copy-Item (Join-Path $src ".github/workflows/gates.yml") $ci }
$co = Join-Path $dst "CODEOWNERS"
if (-not (Test-Path $co)) {
    (Get-Content (Join-Path $src "CODEOWNERS")) -replace "@microphage-create", "@your-gatekeeper" | Set-Content -Encoding utf8NoBOM $co
    Write-Host "CODEOWNERS created: replace @your-gatekeeper with your gatekeeper's handle"
}

# Propagate the MIT license and attribution (techniques/ banks are BMAD, MIT)
foreach ($f in @("LICENSE", "NOTICE.md")) {
    $to = Join-Path $dst $f
    $fromf = Join-Path $src $f
    if ((-not (Test-Path $to)) -and (Test-Path $fromf)) { Copy-Item $fromf $to }
}

# Seed the wiki (INDEX + spaces), never overwriting
$wiki = Join-Path $dst "wiki"
foreach ($d in @("agents", "adr", "projects", "_staging", "_archive", "sessions", "metrics")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $wiki $d) | Out-Null
}
$index = Join-Path $wiki "INDEX.md"
if (-not (Test-Path $index)) {
    @'
# Registry index

One line per artifact: `- [type] id: one-line summary → path`

## Agents

- [service] microwave: agent zero, the desktop front door that opens a context-loaded session on this repo → wiki/agents/microwave.md

## ADR (meta)

## Projects
'@ | Set-Content -Encoding utf8NoBOM $index
}
$register = Join-Path $wiki "sessions/REGISTER.md"
if (-not (Test-Path $register)) {
    @'
# Session save register

Append-only lookup table for `flows/save.md` / `flows/resume.md`. One line
per save, most recent last:

`- S-YYYYMMDD-NN-slug | YYYY-MM-DD | agent | scope | one-line summary`

An id is all a human needs to resume from any machine that has this repo.
Saves live beside this file; this register is their local index (ADR-012).
'@ | Set-Content -Encoding utf8NoBOM $register
}
$ledger = Join-Path $wiki "metrics/LEDGER.md"
if (-not (Test-Path $ledger)) {
    @'
# Governance ledger (append-only)

One line per governance event, logged at the moment it happens (ADR-014).
Format: `DATE | event | subject | detail | author` (author = agent+human).

Events: created (agent activated, detail = minutes) - intercepted (defect
caught before activation, detail = source:severity) - deduped (creation
blocked as duplicate) - purged (agent/atom retired, detail = why).

`gates/metrics.py` aggregates this into the ROI report; `--digest` breaks it
down per author. Never edit past lines: the ledger is history.
'@ | Set-Content -Encoding utf8NoBOM $ledger
}

# CLAUDE.md (session-start context) + agent-zero card, additive (parity with uvx)
# agent-zero card: copy if absent
$cardTo = Join-Path $dst "wiki/agents/microwave.md"
$cardFrom = Join-Path $src "wiki/agents/microwave.md"
if ((-not (Test-Path $cardTo)) -and (Test-Path $cardFrom)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $cardTo) | Out-Null
    Copy-Item $cardFrom $cardTo
}
# session-start context: copy if absent, else append (never clobber), matching uvx
foreach ($ctx in @("CLAUDE.md", "AGENTS.md")) {
    $to = Join-Path $dst $ctx
    $fromf = Join-Path $src $ctx
    if (-not (Test-Path $fromf)) { continue }
    if (-not (Test-Path $to)) {
        Copy-Item $fromf $to
    } elseif (-not (Select-String -Path $to -Pattern "runs on Microwave" -Quiet)) {
        Add-Content -Path $to -Value "`n`n---`n`n$(Get-Content $fromf -Raw)"
    }
}

if ($isRepo) {
    # Wire the hook from the TRUSTED source ($src), never from the target tree.
    # Running $dst/hooks/install-hooks.ps1 would execute a repo-planted script:
    # the exact RCE the uvx path guards against.
    Push-Location $dst
    try { & (Join-Path $src "hooks/install-hooks.ps1") }
    finally { Pop-Location }
}

Write-Host "Microwave installed into $dst (flows, templates, techniques, slop, gates, embodiment, hooks, harness, CI workflow)"
Write-Host "Next: open your coding agent here and run /microwave (or say 'run the Microwave welcome flow')."
Write-Host "Hardening left to you (cannot be shipped as files):"
Write-Host "  1. edit CODEOWNERS with your gatekeeper's handle"
Write-Host "  2. adapt harness/claude-settings.example.json into your harness settings"
Write-Host "  3. enable branch protection requiring the 'gates' check (GitHub repo Settings > Branches, or ask /microwave to walk you through it)."
