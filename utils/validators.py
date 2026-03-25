"""Validation helpers."""

from __future__ import annotations

import pandas as pd



def ensure_datetime(df: pd.DataFrame, column: str) -> list[str]:
    issues: list[str] = []
    try:
        pd.to_datetime(df[column])
    except Exception:
        issues.append(f"Column '{column}' cannot be parsed as datetime")
    return issues


def find_missing_columns(df: pd.DataFrame, required: list[str]) -> list[str]:
    return [col for col in required if col not in df.columns]


def missing_value_ratio(df: pd.DataFrame) -> float:
    return float(df.isna().mean().mean())
