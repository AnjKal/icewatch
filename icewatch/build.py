from __future__ import annotations

from pathlib import Path
import json

from .core import build_demo_payload


def main() -> None:
    payload = build_demo_payload()
    Path("site/data").mkdir(parents=True, exist_ok=True)
    print(json.dumps({
        "dataset_file": payload["dataset"]["track_file"],
        "track_points": payload["dataset"]["track_points"],
        "routes": payload["routes"],
    }, indent=2))


if __name__ == "__main__":
    main()

