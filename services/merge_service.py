"""Merge service for master dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from models.dataset_model import MASTER_COLUMNS


class MergeService:
    """Build final master dataset from harmonized files."""

    def build_master(self, harmonized_files: list[Path]) -> pd.DataFrame:
        if not harmonized_files:
            return pd.DataFrame(columns=MASTER_COLUMNS)
        frames = [pd.read_parquet(path) for path in harmonized_files]
        combined = pd.concat(frames, ignore_index=True)
        combined = combined.drop_duplicates(subset=["timestamp", "scenario_id", "run_id", "labels"]) 
        for col in MASTER_COLUMNS:
            if col not in combined.columns:
                combined[col] = None
        return combined[MASTER_COLUMNS]
