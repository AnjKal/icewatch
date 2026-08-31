Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
$venv = Join-Path (Split-Path -Parent $repo) '.venv\Scripts\python.exe'
Set-Location $repo

& $venv tools\build_manifest.py
& $venv -m icewatch.build
