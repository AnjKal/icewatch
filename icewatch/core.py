from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import math
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "icebergs_v5" / "consol"
OUT_DIR = ROOT / "site" / "data"


@dataclass
class TrackPoint:
    date: int
    lat: float
    lon: float
    confidence: float
    source: str


def parse_float(value: str) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except ValueError:
        return None


def load_track(path: Path) -> list[TrackPoint]:
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    points: list[TrackPoint] = []
    for row in rows:
        date_raw = row.get("date", "")
        try:
            date = int(float(date_raw))
        except ValueError:
            continue

        lat = None
        lon = None
        source = "unknown"
        for prefix in ("nic", "sass", "ascat", "oscat", "qscat", "seawinds", "ers", "nscat"):
            a = parse_float(row.get(f"{prefix}_1", ""))
            b = parse_float(row.get(f"{prefix}_2", ""))
            if a is not None and b is not None and a != 0 and b != 0:
                lat, lon, source = a, b, prefix
                break
        if lat is None or lon is None:
            continue
        size_a = parse_float(row.get("size_1", ""))
        size_b = parse_float(row.get("size_2", ""))
        conf = 0.5
        if size_a is not None or size_b is not None:
            conf = min(1.0, 0.35 + 0.02 * ((size_a or 0) + (size_b or 0)))
        points.append(TrackPoint(date=date, lat=lat, lon=lon, confidence=conf, source=source))
    return points


def pick_demo_track() -> tuple[Path, list[TrackPoint]]:
    candidates = []
    for path in DATA_DIR.glob("*.csv"):
        points = load_track(path)
        if len(points) >= 3:
            candidates.append((path, points))
    candidates.sort(key=lambda item: len(item[1]), reverse=True)
    if not candidates:
        raise RuntimeError("No usable iceberg track found")
    return candidates[0]


def forecast_track(points: list[TrackPoint], horizons=(6, 12, 24, 72)) -> list[dict]:
    p1, p2 = points[-2], points[-1]
    dlat = p2.lat - p1.lat
    dlon = p2.lon - p1.lon
    results = []
    for h in horizons:
        steps = max(1, h / 6)
        lat = p2.lat + dlat * steps
        lon = p2.lon + dlon * steps
        confidence = max(0.1, min(0.95, p2.confidence - 0.03 * steps))
        results.append({"horizon_hours": h, "lat": round(lat, 4), "lon": round(lon, 4), "confidence": round(confidence, 2)})
    return results


def build_sea_ice_summary(points: list[TrackPoint]) -> dict:
    lats = [p.lat for p in points]
    lons = [p.lon for p in points]
    center = {"lat": round(mean(lats), 4), "lon": round(mean(lons), 4)}
    spread = round((max(lats) - min(lats)) + (max(lons) - min(lons)), 3)
    risk = min(1.0, 0.28 + spread / 250)
    return {
        "center": center,
        "spread": spread,
        "ice_concentration_index": round(risk, 2),
        "trend": "rising" if spread > 0.8 else "stable",
    }


def route_candidates(track: list[TrackPoint]) -> list[dict]:
    p = track[-1]
    base = [
        {"name": "Route A", "distance_km": 412, "risk": 0.72, "eta_hours": 31.2},
        {"name": "Route B", "distance_km": 468, "risk": 0.33, "eta_hours": 35.4},
        {"name": "Route C", "distance_km": 435, "risk": 0.51, "eta_hours": 33.1},
    ]
    for item in base:
        item["anchor_lat"] = round(p.lat, 4)
        item["anchor_lon"] = round(p.lon, 4)
    return base


def build_demo_payload() -> dict:
    path, points = pick_demo_track()
    sea_ice = build_sea_ice_summary(points)
    forecast = forecast_track(points)
    routes = route_candidates(points)
    payload = {
        "dataset": {
            "track_file": path.name,
            "track_points": len(points),
            "first_date": points[0].date,
            "last_date": points[-1].date,
            "sources": sorted({p.source for p in points}),
        },
        "sea_ice": sea_ice,
        "forecast": forecast,
        "routes": routes,
        "alerts": [
            {
                "severity": "danger",
                "title": "Iceberg trajectory enters transit window",
                "detail": f"{path.name} now projects into the risk corridor within 24 hours.",
            },
            {
                "severity": "caution",
                "title": "Sea-ice index trending upward",
                "detail": "Weighted sea-ice risk is rising in the current sector.",
            },
            {
                "severity": "safe",
                "title": "Route B remains the safest option",
                "detail": "Lower combined risk despite slightly longer travel distance.",
            },
        ],
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "demo.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
