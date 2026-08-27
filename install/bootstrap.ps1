# Microwave one-line installer (Windows, PowerShell 7+):
#   irm https://raw.githubusercontent.com/microphage-create/microwave-method/main/install/bootstrap.ps1 | iex
# Installs into the CURRENT directory; set $env:MICROWAVE_TARGET to override.
# This clones and executes a branch at HEAD: pin it with $env:MICROWAVE_REF =
# "<branch|tag>", or download this file, read it, then run it.
# (#Requires does not apply under iex, hence the explicit version guard.)
$ErrorActionPreference = "Stop"

if ($PSVersionTable.PSVersion.Major -lt 7) {
    throw "PowerShell 7+ is required (you are on $($PSVersionTable.PSVersion)): https://aka.ms/powershell"
}

$target = if ($env:MICROWAVE_TARGET) { $env:MICROWAVE_TARGET } else { (Get-Location).Path }
$ref = if ($env:MICROWAVE_REF) { $env:MICROWAVE_REF } else { "main" }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git is required" }

# A real interpreter check: the Windows Store alias fakes `python` on PATH,
# and the version must actually be 3.10+.
$py = @("python3", "python", "py") | Where-Object {
    $v = & $_ --version 2>$null
    $LASTEXITCODE -eq 0 -and $v -match "Python 3\.(1[0-9]|[2-9][0-9])"
} | Select-Object -First 1
if (-not $py) { throw "Python 3.10+ is required (a working python3/python/py on PATH)" }

$tmp = Join-Path ([IO.Path]::GetTempPath()) ("microwave-" + [guid]::NewGuid().ToString("N").Substring(0, 8))
try {
    Write-Host "Fetching Microwave Method ($ref)..."
    git clone --quiet --depth 1 --branch $ref https://github.com/microphage-create/microwave-method $tmp
    if ($LASTEXITCODE -ne 0) { throw "git clone failed (exit $LASTEXITCODE): check network access" }
    & (Join-Path $tmp "install/install.ps1") -Target $target
}
finally {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Done. Next: open your coding agent in $target and run /microwave"
Write-Host '  (or say "run the Microwave welcome flow" - guides you, scans your existing agents)'
