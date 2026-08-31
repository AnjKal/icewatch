from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "icebergs_v5" / "consol"


def logical_name(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_").lower()
    return f"track_{stem}.csv"


def main() -> None:
    files = sorted(DATA_DIR.glob("*.csv"))
    for path in files:
        target = path.with_name(logical_name(path))
        if path.name == target.name:
            continue
        if target.exists():
            raise FileExistsError(f"Target already exists: {target}")
        path.rename(target)


if __name__ == "__main__":
    main()
