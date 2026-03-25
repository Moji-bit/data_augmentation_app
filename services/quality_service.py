"""Data quality profiling service."""

from __future__ import annotations

import numpy as np
import pandas as pd


class QualityService:
    """Compute quality metrics and ratings."""

    def profile(self, measurements: pd.DataFrame, events: pd.DataFrame, actuators: pd.DataFrame) -> dict:
        metric = {
            "missing_values": float(measurements.isna().mean().mean()),
            "signal_variance_mean": float(measurements.select_dtypes(include=[np.number]).var().mean()),
            "event_frequency": int(len(events)),
            "sensor_coverage": int(measurements["tag"].nunique()) if "tag" in measurements else 0,
            "actuator_coverage": int(actuators["actuator_tag"].nunique()) if "actuator_tag" in actuators else 0,
            "dataset_rows": int(len(measurements) + len(events) + len(actuators)),
            "class_distribution": events["event_type"].value_counts(dropna=False).to_dict()
            if "event_type" in events
            else {},
        }
        quality = "hoch" if metric["missing_values"] < 0.05 else "mittel" if metric["missing_values"] < 0.15 else "niedrig"
        ml = "gut" if metric["sensor_coverage"] >= 3 else "eingeschränkt" if metric["sensor_coverage"] >= 2 else "schlecht"
        metric["data_quality"] = quality
        metric["ml_readiness"] = ml
        return metric
