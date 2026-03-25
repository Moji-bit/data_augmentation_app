"""Package ingestion service."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pandas as pd

from utils.constants import RAW_DIR, REQUIRED_FILES


class IngestionService:
    """Copy package files into managed storage and parse metadata."""

    def ingest_package(self, package_dir: Path) -> dict:
        missing = [name for name in REQUIRED_FILES if not (package_dir / name).exists()]
        if missing:
            raise ValueError(f"Package is incomplete, missing: {missing}")

        scenario_data = json.loads((package_dir / "scenario.json").read_text(encoding="utf-8"))
        scenario_id = scenario_data.get("scenario_id", "unknown_scenario")
        run_id = scenario_data.get("run_id") or f"run_{uuid4().hex[:8]}"
        package_id = f"pkg_{uuid4().hex[:10]}"

        target = RAW_DIR / package_id
        target.mkdir(parents=True, exist_ok=True)
        for name in REQUIRED_FILES:
            shutil.copy2(package_dir / name, target / name)

        return {
            "package_id": package_id,
            "scenario_id": scenario_id,
            "run_id": run_id,
            "import_timestamp": datetime.now(timezone.utc).isoformat(),
            "schema_version": scenario_data.get("schema_version", "1.0"),
        }

    @staticmethod
    def load_package_tables(package_path: Path) -> dict[str, pd.DataFrame]:
        return {
            "measurements_long.csv": pd.read_csv(package_path / "measurements_long.csv"),
            "events.csv": pd.read_csv(package_path / "events.csv"),
            "actuators.csv": pd.read_csv(package_path / "actuators.csv"),
        }
