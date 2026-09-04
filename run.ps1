# Launch the Aggregate Working Platform Streamlit dashboard.
#   Usage:  .\run.ps1            (from the repo root, in PowerShell)
# Stop it with Ctrl+C.
#
# Streamlit apps must be started via "streamlit run", not "python streamlit_app.py".
# This script finds a Python interpreter that actually has streamlit installed and
# uses it, so you don't have to remember the full path.

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

# Candidate interpreters, most-likely first. The pythoncore-3.14-64 install is the
# one with streamlit + anthropic on this machine (see CLAUDE.md).
$candidates = @(
    "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe"
)

function Test-HasStreamlit($exe) {
    if (-not (Test-Path $exe)) { return $false }
    & $exe -c "import streamlit" 2>$null
    return ($LASTEXITCODE -eq 0)
}

$python = $null
foreach ($c in $candidates) {
    if (Test-HasStreamlit $c) { $python = $c; break }
}

if (-not $python) {
    Write-Error ("No Python interpreter with 'streamlit' installed was found. " +
        "Install deps with:  & `"$($candidates[0])`" -m pip install -r requirements.txt")
    exit 1
}

Write-Host "Using $python" -ForegroundColor DarkGray
& $python -m streamlit run streamlit_app.py @args
