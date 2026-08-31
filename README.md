# ICEWATCH

Antarctic maritime decision-support demo for Smart India Hackathon 2026 Problem Statement 59.

## What this repo contains

- `PS.pdf` - the SIH problem statement at the repo root.
- `icewatch/` - the core prototype package with dataset loading and demo generation.
- `site/` - the pitch/demo web app.
- `tools/` - helpers to build dataset manifests.
- `vercel.json` - Vercel routing config for the demo site.

## What the demo shows

- The SIH problem statement and project scope.
- Local iceberg datasets already present in the repository.
- External datasets and benchmarks useful for the pitch.
- A generated model-output view based on the local Antarctic tracks.
- Route comparison, alerts, and a system architecture summary.

## Local setup

This project is designed to run from the repository root and use the local virtual environment.

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

### 4. Open the site locally

You can open `site/index.html` directly in a browser, or serve the repo with any static server.

## Scripts

Use the scripts in `scripts/` for repeatable local tasks.

- `scripts/build.ps1` - rebuild the generated demo JSON and manifest.
- `scripts/dev.ps1` - start a local static server for the `site/` folder.
- `scripts/check.ps1` - run quick syntax/build verification.

## Vercel deployment

This repository already includes `vercel.json`, which rewrites `/` to `site/index.html`.

### Option A: Import from the Vercel dashboard

1. Sign in to Vercel.
2. Create a new project and import the GitHub repository.
3. Set the root to the repository root.
4. Leave the build command empty, because this is a static site.
5. Set the output to the `site/` folder if needed, or rely on the rewrite config.
6. Deploy.

### Option B: Vercel CLI

```powershell
npm i -g vercel
vercel login
vercel
vercel --prod
```

### If the repo is private

- Make sure the GitHub account that owns or is invited to the repo has access to the repo.
- Connect GitHub to Vercel from the Vercel dashboard first.
- If the repository is under a personal GitHub account, Vercel’s GitHub import flow expects the repository owner for initial configuration. If you are only a contributor, ask the owner to connect/import it or add you with the correct Vercel team/project role. citeturn0search0turn0search2turn0search14
- Once connected, Vercel will auto-deploy supported Git repos on branch pushes and PR updates. citeturn0search1turn0search6

## Project status

This repo already has:

- a polished pitch site
- generated dataset manifests
- a working heuristic drift/risk prototype
- Vercel configuration
- the SIH problem statement renamed to `PS.pdf`

## Next upgrades

- Real trained sea-ice and iceberg forecast models
- Proper graph-based route optimizer
- Better visualizations and map overlays
- Evaluation metrics and benchmark charts
- A more complete demo backend if live data is added later

