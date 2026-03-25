"""Data harmonization service."""

from __future__ import annotations

import json

import pandas as pd


class HarmonizationService:
    """Transform and join tables into harmonized master frame."""

    def long_to_wide(self, measurements: pd.DataFrame) -> pd.DataFrame:
        wide = measurements.pivot_table(
            index=["timestamp", "scenario_id"], values="value", columns="tag", aggfunc="mean"
        ).reset_index()
        wide.columns.name = None
        return wide

    def build_harmonized(
        self,
        measurements: pd.DataFrame,
        events: pd.DataFrame,
        actuators: pd.DataFrame,
        scenario_meta: dict,
        run_id: str,
        is_augmented: bool = False,
        augmentation_method: str = "none",
    ) -> pd.DataFrame:
        sensor_wide = self.long_to_wide(measurements)
        actuator_wide = actuators.pivot_table(
            index=["timestamp", "scenario_id"], values="value", columns="actuator_tag", aggfunc="mean"
        ).reset_index()
        actuator_wide.columns.name = None

        merged = sensor_wide.merge(actuator_wide, on=["timestamp", "scenario_id"], how="outer", suffixes=("", "_act"))
        merged = merged.merge(events, on=["timestamp", "scenario_id"], how="left")

        sensor_cols = [c for c in sensor_wide.columns if c not in {"timestamp", "scenario_id"}]
        actuator_cols = [c for c in actuator_wide.columns if c not in {"timestamp", "scenario_id"}]

        merged["run_id"] = run_id
        merged["sensor_features"] = merged[sensor_cols].apply(lambda r: json.dumps(r.dropna().to_dict()), axis=1)
        merged["actuator_features"] = merged[actuator_cols].apply(lambda r: json.dumps(r.dropna().to_dict()), axis=1)
        merged["metadata"] = json.dumps(scenario_meta)
        merged["labels"] = merged["event_type"].fillna("none") if "event_type" in merged else "none"
        merged["is_augmented"] = is_augmented
        merged["augmentation_method"] = augmentation_method
        return merged
