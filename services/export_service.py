"""Export service."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class ExportService:
    """Handle artifact export."""

    @staticmethod
    def export_parquet(df: pd.DataFrame, out_path: Path) -> Path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out_path, index=False)
        return out_path
