"""Data lineage service."""

from __future__ import annotations

import pandas as pd


class LineageService:
    """Build lineage summaries from registry."""

    @staticmethod
    def summarize(registry_df: pd.DataFrame) -> pd.DataFrame:
        if registry_df.empty:
            return pd.DataFrame(columns=["metric", "value"])
        return pd.DataFrame(
            [
                {"metric": "packages_total", "value": len(registry_df)},
                {
                    "metric": "packages_augmented",
                    "value": int((registry_df["augmentation_status"] == "done").sum()),
                },
                {
                    "metric": "included_in_master",
                    "value": int(registry_df["included_in_master_dataset"].sum()),
                },
            ]
        )
