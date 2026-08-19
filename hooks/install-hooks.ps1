#Requires -Version 7
# Installs the Microwave pre-commit hook into the current repo (Windows).
# Handles worktrees, submodules and core.hooksPath via git rev-parse.
# Never silently overwrites an existing hook: it is backed up first.
$ErrorActionPreference = "Stop"

git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) { throw "install-hooks: not inside a git repository" }

$hooksDir = git rev-parse --git-path hooks
if ($LASTEXITCODE -ne 0 -or -not $hooksDir) { throw "install-hooks: cannot resolve hooks path" }
New-Item -ItemType Directory -Force -Path $hooksDir | Out-Null

$source = Join-Path $PSScriptRoot "pre-commit"
$target = Join-Path $hooksDir "pre-commit"
if ((Test-Path $target) -and (Get-FileHash $source).Hash -ne (Get-FileHash $target).Hash) {
    Copy-Item $target "$target.pre-microwave"
    Write-Host "existing pre-commit hook backed up to $target.pre-microwave"
    Write-Host "(chain it by calling it from the new hook if you still need it)"
}
Copy-Item $source $target
Write-Host "pre-commit hook installed at ${target}: gates run on staged agent cards"
