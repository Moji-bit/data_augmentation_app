"""Registry module."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils.constants import REGISTRY_FILE


class Registry:
    COLUMNS = [
        "package_id",
        "scenario_id",
        "run_id",
        "import_timestamp",
        "validation_status",
        "augmentation_status",
        "included_in_master_dataset",
        "schema_version",
    ]

    def load(self) -> pd.DataFrame:
        if not REGISTRY_FILE.exists():
            return pd.DataFrame(columns=self.COLUMNS)
        return pd.read_csv(REGISTRY_FILE)

    def upsert(self, record: dict) -> pd.DataFrame:
        df = self.load()
        df = df[df["package_id"] != record["package_id"]] if not df.empty else df
        new_df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        new_df.to_csv(REGISTRY_FILE, index=False)
        return new_df

    def update_status(self, package_id: str, **updates) -> pd.DataFrame:
        df = self.load()
        for key, value in updates.items():
            df.loc[df["package_id"] == package_id, key] = value
        df.to_csv(REGISTRY_FILE, index=False)
        return df
