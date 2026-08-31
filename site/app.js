const resources = [
  {
    title: 'BYU/NIC Antarctic iceberg database',
    meta: 'Iceberg tracks',
    desc: 'Consolidated iceberg positions from scatterometer and NIC sources. Useful for trajectory baselines and track interpolation.'
  },
  {
    title: 'AI4Arctic / ASIP sea-ice dataset',
    meta: 'Sea-ice segmentation',
    desc: 'Sentinel-1 SAR sea-ice mapping benchmark for pretraining or transfer learning before Antarctica-specific fine-tuning.'
  },
  {
    title: 'Copernicus Marine Antarctic sea-ice products',
    meta: 'Operational ocean data',
    desc: 'Sea-ice concentration and related marine conditions for building forecast features and live-style demo layers.'
  },
  {
    title: 'ERA5 reanalysis',
    meta: 'Atmospheric forcing',
    desc: 'Wind, pressure, temperature, and wave features that help explain iceberg drift and sea-ice evolution.'
  },
  {
    title: 'IDRIFTNET',
    meta: 'Model benchmark',
    desc: 'Physics-driven iceberg drift forecasting reference with ADE/FDE-style evaluation on Antarctic icebergs.'
  },
  {
    title: 'Route optimization literature',
    meta: 'Decision support',
    desc: 'Graph-based routing with Dijkstra or A* can turn forecast outputs into navigable safe-path recommendations.'
  }
];

const features = [
  ['Forecast view', 'Sea-ice change, iceberg drift, and route risk over short horizons.'],
  ['Explainability', 'Show why a path is risky using ice concentration, proximity, and uncertainty.'],
  ['Fallback mode', 'Physics-first drift estimate when a learned model is not available.'],
  ['Multi-source input', 'Local tracks plus SAR, weather, and ocean features in one pipeline.'],
  ['Demo-friendly UI', 'A strong visual story for judges without requiring live satellite access.'],
  ['Scalable architecture', 'Designed so the same pipeline can later be connected to live data feeds.']
];

const workflow = [
  'Load Antarctic iceberg tracks and sea-ice reference data from this repository.',
  'Merge in weather and ocean forcing features such as wind and sea state.',
  'Forecast iceberg drift and sea-ice concentration at 6h, 12h, 24h, and 3-day horizons.',
  'Convert the region into a weighted navigation graph with risk scores on nodes and edges.',
  'Run shortest-path search to find the safest and most efficient route.',
  'Render the result in a dashboard with forecasts, alerts, and an explanation panel.'
];

const problemPills = [
  'Sea-ice forecasting',
  'Iceberg trajectory prediction',
  'Navigation risk analysis'
];

const pitchCards = [
  ['Why it matters', 'Antarctic shipping needs forward-looking risk, not static charts.'],
  ['What we built', 'A decision-support demo using local tracks, forecasts, and route scoring.'],
  ['Why it is credible', 'Uses public polar data, proven benchmarks, and a physics-first fallback.']
];

const architectureCards = [
  ['Data layer', 'Local iceberg CSVs, sea-ice references, and external weather/ocean sources.'],
  ['Inference layer', 'Track extrapolation, sea-ice risk estimation, and route ranking.'],
  ['Presentation layer', 'A polished pitch site with dataset proofs, outputs, and demo narratives.']
];

async function loadManifest() {
  const res = await fetch('./data/manifest.json');
  return res.json();
}

async function loadDemo() {
  const res = await fetch('./data/demo.json');
  return res.json();
}

function render() {
  const heroStats = document.getElementById('heroStats');
  const datasetMetrics = document.getElementById('datasetMetrics');
  const datasetTable = document.getElementById('datasetTable');
  const featureGrid = document.getElementById('featureGrid');
  const resourceList = document.getElementById('resources');
  const workflowList = document.getElementById('workflow');
  const problem = document.getElementById('problemPills');
  const pitchGrid = document.getElementById('pitchGrid');
  const archGrid = document.getElementById('archGrid');
  const routeTable = document.getElementById('routeTable');

  problem.innerHTML = problemPills.map((text) => `<div class="pill">${text}</div>`).join('');
  pitchGrid.innerHTML = pitchCards.map(([title, desc]) => `<div class="pitch-card"><strong>${title}</strong><p>${desc}</p></div>`).join('');
  archGrid.innerHTML = architectureCards.map(([title, desc]) => `<div class="arch-card"><strong>${title}</strong><p>${desc}</p></div>`).join('');
  workflowList.innerHTML = workflow.map((step, idx) => `<li><strong>Step ${idx + 1}:</strong> ${step}</li>`).join('');
  featureGrid.innerHTML = features.map(([title, desc]) => `<div class="feature"><strong>${title}</strong><div>${desc}</div></div>`).join('');
  resourceList.innerHTML = resources.map((r) => `<article class="resource"><div class="meta">${r.meta}</div><div class="title">${r.title}</div><div class="desc">${r.desc}</div></article>`).join('');
}

function humanBytes(bytes) {
  const units = ['B', 'KB', 'MB', 'GB'];
  let value = bytes;
  let idx = 0;
  while (value >= 1024 && idx < units.length - 1) {
    value /= 1024;
    idx += 1;
  }
  return `${value.toFixed(value >= 10 ? 0 : 1)} ${units[idx]}`;
}

Promise.all([loadManifest(), loadDemo()]).then(([manifest, demo]) => {
  render();

  document.getElementById('heroStats').innerHTML = [
    { label: 'CSV files', value: manifest.csv_count, hint: 'Raw iceberg-track files already in repo' },
    { label: 'Repository data', value: humanBytes(manifest.total_size_bytes), hint: 'Local Antarctic CSV archive' },
    { label: 'Largest file', value: manifest.largest_files[0].name, hint: `${manifest.largest_files[0].columns} columns` },
    { label: 'Route logic', value: 'Graph-based', hint: 'Risk-aware shortest-path planning' }
  ].map((item) => `
    <div class="stat">
      <div class="label">${item.label}</div>
      <div class="value">${item.value}</div>
      <div class="hint">${item.hint}</div>
    </div>
  `).join('');

  document.getElementById('datasetMetrics').innerHTML = [
    { label: 'CSV count', value: manifest.csv_count, sub: 'Files under icebergs_v5/consol' },
    { label: 'Common columns', value: manifest.common_columns.length, sub: 'Shared fields across files' },
    { label: 'Sampled files', value: manifest.samples.length, sub: 'Representative previews' }
  ].map((item) => `
    <div class="metric">
      <div class="label">${item.label}</div>
      <div class="value">${item.value}</div>
      <div class="sub">${item.sub}</div>
    </div>
  `).join('');

  const sampleRows = manifest.samples.map((file) => {
    const preview = file.sample[0] ? file.sample[0].slice(0, 6).join(', ') : 'No preview';
    return `<tr><td><strong>${file.name}</strong><div class="sub">${file.header.slice(0, 8).join(', ')}${file.header.length > 8 ? ', ...' : ''}</div></td><td>${file.header.length}</td><td>${preview}</td></tr>`;
  }).join('');
  datasetTable.innerHTML = sampleRows;

  document.getElementById('demoSummary').innerHTML = `
    <div class="demo-card">
      <div class="badge safe">Track file</div>
      <h3>${demo.dataset.track_file}</h3>
      <div class="meta">Points: ${demo.dataset.track_points} | Dates: ${demo.dataset.first_date} to ${demo.dataset.last_date}</div>
      <div class="desc">Sources: ${demo.dataset.sources.join(', ')}</div>
    </div>
    <div class="demo-card">
      <div class="badge caution">Sea-ice index</div>
      <h3>${demo.sea_ice.ice_concentration_index}</h3>
      <div class="meta">Trend: ${demo.sea_ice.trend}</div>
      <div class="desc">Center: ${demo.sea_ice.center.lat}, ${demo.sea_ice.center.lon} | Spread: ${demo.sea_ice.spread}</div>
    </div>
    <div class="demo-card">
      <div class="badge danger">Route ranking</div>
      <h3>${demo.routes[0].name} vs ${demo.routes[1].name}</h3>
      <div class="meta">Lowest risk route is highlighted as the safe option.</div>
      <div class="desc">This shows the decision-support logic rather than autonomous control.</div>
    </div>
    <div class="demo-card">
      <div class="badge safe">Prediction horizon</div>
      <h3>${demo.forecast.map((f) => `${f.horizon_hours}h`).join(' / ')}</h3>
      <div class="meta">Short-range drift outputs</div>
      <div class="desc">Forecasts are generated from the selected track's motion trend and confidence decay.</div>
    </div>
  `;

  document.getElementById('demoAlerts').innerHTML = demo.alerts.map((item) => `
    <div class="demo-card">
      <div class="badge ${item.severity}">${item.severity}</div>
      <h3>${item.title}</h3>
      <div class="desc">${item.detail}</div>
    </div>
  `).join('');

  const routeRows = demo.routes.map((route) => `
    <tr>
      <td><strong>${route.name}</strong></td>
      <td>${route.distance_km}</td>
      <td>${route.risk}</td>
      <td>${route.eta_hours}</td>
    </tr>
  `).join('');
  routeTable.innerHTML = routeRows;
}).catch((err) => {
  console.error(err);
  document.body.insertAdjacentHTML('beforeend', '<div style="padding:24px;color:#fff">Failed to load manifest.json. Run tools/build_manifest.py first.</div>');
  render();
});
