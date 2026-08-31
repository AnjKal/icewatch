Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
$venv = Join-Path (Split-Path -Parent $repo) '.venv\Scripts\python.exe'
Set-Location $repo

Write-Host "Serving site/ on http://localhost:8000"
& $venv -m http.server 8000 -d site
