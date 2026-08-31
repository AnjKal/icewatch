from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "icebergs_v5" / "consol"
OUTPUT = ROOT / "site" / "data" / "manifest.json"


def read_csv_preview(path: Path, rows: int = 3):
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        sample = []
        for _ in range(rows):
            try:
                sample.append(next(reader))
            except StopIteration:
                break
    return header, sample


def main() -> None:
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    sizes = []
    col_counts = Counter()
    samples = []

    for path in csv_files:
        size = path.stat().st_size
        header, sample = read_csv_preview(path)
        sizes.append(
            {
                "name": path.name,
                "size_bytes": size,
                "columns": len(header),
                "header": header,
                "sample": sample,
            }
        )
        if header:
            col_counts.update(header)
        if len(samples) < 12 and header:
            samples.append(
                {
                    "name": path.name,
                    "header": header,
                    "sample": sample,
                }
            )

    largest = sorted(sizes, key=lambda x: x["size_bytes"], reverse=True)[:12]

    manifest = {
        "dataset_root": str(DATA_DIR.relative_to(ROOT)).replace("\\", "/"),
        "csv_count": len(csv_files),
        "total_size_bytes": sum(item["size_bytes"] for item in sizes),
        "largest_files": largest,
        "common_columns": col_counts.most_common(20),
        "samples": samples,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
