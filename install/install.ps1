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
    Write-Host "warning: $dst is not a git repository (gates rely on repo protection)" -ForegroundColor Yellow
}

$dirs = @("flows", "templates", "techniques", "slop", "gates", "embodiment", "hooks", "harness")
foreach ($d in $dirs) {
    $from = Join-Path $src $d
    $to = Join-Path $dst $d
    New-Item -ItemType Directory -Force -Path $to | Out-Null
    Get-ChildItem -Recurse -File $from | Where-Object { $_.FullName -notmatch '[\\/]icons[\\/]' } | ForEach-Object {
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

# Seed the wiki (INDEX + spaces), never overwriting
$wiki = Join-Path $dst "wiki"
foreach ($d in @("agents", "adr", "projects", "_staging", "_archive")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $wiki $d) | Out-Null
}
$index = Join-Path $wiki "INDEX.md"
if (-not (Test-Path $index)) {
    @'
# Registry index

One line per artifact: `- [type] id: one-line summary → path`

## Agents

## ADR (meta)

## Projects
'@ | Set-Content -Encoding utf8NoBOM $index
}

if ($isRepo) {
    Push-Location $dst
    try { & (Join-Path $dst "hooks/install-hooks.ps1") }
    finally { Pop-Location }
}

Write-Host "Microwave installed into $dst (flows, templates, techniques, slop, gates, embodiment, hooks, harness, CI workflow)"
Write-Host "Next: open your coding agent there and say 'run the Microwave adopt flow'."
Write-Host "Hardening left to you (cannot be shipped as files):"
Write-Host "  1. edit CODEOWNERS with your gatekeeper's handle"
Write-Host "  2. adapt harness/claude-settings.example.json into your harness settings"
Write-Host "  3. enable branch protection with required check 'gates' (gh api ... enforce_admins=true)"
