"""Build example dataset_master.parquet from sample_data.
Run after installing requirements.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from services.harmonization_service import HarmonizationService
from services.merge_service import MergeService


def main() -> None:
    harm = HarmonizationService()
    harmonized_files: list[Path] = []
    for package in [Path("sample_data/package_001"), Path("sample_data/package_002")]:
        m = pd.read_csv(package / "measurements_long.csv")
        e = pd.read_csv(package / "events.csv")
        a = pd.read_csv(package / "actuators.csv")
        meta = json.loads((package / "scenario.json").read_text(encoding="utf-8"))
        run_id = meta.get("run_id", "run_generated")
        h = harm.build_harmonized(m, e, a, meta, run_id=run_id)
        out = Path("storage/harmonized") / f"{package.name}.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        h.to_parquet(out, index=False)
        harmonized_files.append(out)

    master = MergeService().build_master(harmonized_files)
    final = Path("storage/final/dataset_master.parquet")
    final.parent.mkdir(parents=True, exist_ok=True)
    master.to_parquet(final, index=False)
    print(f"Wrote {final}")


if __name__ == "__main__":
    main()
