"""Reporting module."""

from __future__ import annotations

import pandas as pd


class ReportModule:
    def build_markdown(self, registry_df: pd.DataFrame, quality: dict | None) -> str:
        lines = ["# Data Platform Report", "", f"Packages: {len(registry_df)}"]
        if quality:
            lines.append(f"Data Quality: {quality.get('data_quality')}")
            lines.append(f"ML Readiness: {quality.get('ml_readiness')}")
        return "\n".join(lines)
