# ICEWATCH

A decision-support platform for Antarctic navigation, built for Smart India Hackathon 2026 Problem Statement 59.

## What this repo contains

- `PS.pdf` - the SIH problem statement at the repo root.
- `icewatch/` - the core prototype package with dataset loading and output generation.
- `site/` - the pitch and demo web app.
- `tools/` - helpers to build dataset manifests.
- `vercel.json` - static hosting routing config.

## Product highlights

- Sea-ice concentration and short-range change
- Iceberg trajectory forecasting
- Risk-aware route comparison
- Explainable alerts and confidence indicators
- Curated references and benchmarks for pitching

## Local setup

The project runs from the repository root and uses the local virtual environment.

### 1. Create the venv

```powershell
python -m venv .venv
```

### 2. Activate the venv

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\\.venv\\Scripts\\Activate.ps1
```

### 3. Build the demo data

```powershell
python -m icewatch.build
```

This generates:

- `site/data/manifest.json`
- `site/data/demo.json`

## Scripts

- `scripts/build.ps1` - rebuild the generated demo JSON and manifest.
- `scripts/dev.ps1` - start a local static server for the `site/` folder.
- `scripts/check.ps1` - run quick syntax/build verification.

## Project status

- polished pitch and demo pages
- generated dataset manifests
- a heuristic drift/risk prototype
- static hosting configuration
- the SIH problem statement renamed to `PS.pdf`

## Next upgrades

- Real trained sea-ice and iceberg forecast models
- Proper graph-based route optimizer
- Better visualizations and map overlays
- Evaluation metrics and benchmark charts
- A more complete demo backend if live data is added later
