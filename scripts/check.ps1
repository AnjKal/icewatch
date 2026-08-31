Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
$venv = Join-Path (Split-Path -Parent $repo) '.venv\Scripts\python.exe'
Set-Location $repo

& $venv -m py_compile icewatch\core.py icewatch\build.py tools\build_manifest.py
node --check site\app.js
