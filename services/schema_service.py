"""Schema validation and drift service."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from utils.constants import EXPECTED_COLUMNS
from utils.validators import ensure_datetime, find_missing_columns


@dataclass
class SchemaCheckResult:
    valid: bool
    issues: list[str]
    warnings: list[str]


class SchemaService:
    """Validate package input schemas and detect drift."""

    def validate_table(self, filename: str, df: pd.DataFrame) -> SchemaCheckResult:
        issues: list[str] = []
        warnings: list[str] = []
        required = EXPECTED_COLUMNS.get(filename, [])
        missing = find_missing_columns(df, required)
        if missing:
            issues.append(f"{filename} missing columns: {missing}")
        if "timestamp" in df.columns:
            issues.extend(ensure_datetime(df, "timestamp"))
        optional = sorted(set(df.columns) - set(required))
        if optional:
            warnings.append(f"{filename} optional/drift columns: {optional}")
        if "scenario_id" in df.columns and df["scenario_id"].isna().any():
            issues.append(f"{filename}: scenario_id contains missing values")
        return SchemaCheckResult(valid=not issues, issues=issues, warnings=warnings)

    def compare_schema(self, reference_df: pd.DataFrame, candidate_df: pd.DataFrame) -> list[str]:
        ref_cols = set(reference_df.columns)
        cand_cols = set(candidate_df.columns)
        warnings = []
        if ref_cols != cand_cols:
            warnings.append(
                f"Schema drift detected. Added={sorted(cand_cols-ref_cols)} Removed={sorted(ref_cols-cand_cols)}"
            )
        return warnings
