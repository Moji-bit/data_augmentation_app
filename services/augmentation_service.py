"""Augmentation service."""

from __future__ import annotations

import numpy as np
import pandas as pd

from models.config_model import AugmentationConfig


class AugmentationService:
    """Apply deterministic/controlled augmentations."""

    def augment(self, measurements: pd.DataFrame, events: pd.DataFrame, actuators: pd.DataFrame, config: AugmentationConfig):
        m = measurements.copy()
        e = events.copy()
        a = actuators.copy()

        rng = np.random.default_rng(42)
        if "jitter" in config.enabled and "value" in m:
            m["value"] = m["value"] + rng.normal(0, config.jitter_std, len(m))
        if "scaling" in config.enabled and "value" in m:
            factor = rng.uniform(config.scaling_min, config.scaling_max)
            m["value"] = m["value"] * factor
        if "noise" in config.enabled and "value" in m:
            m["value"] = m["value"] + rng.normal(0, config.noise_std, len(m))
        if "event_shift" in config.enabled and "timestamp" in e:
            e["timestamp"] = pd.to_datetime(e["timestamp"]) + pd.to_timedelta(config.event_shift_steps, unit="s")
        if "severity_scaling" in config.enabled and "severity" in e:
            e["severity"] = e["severity"].astype(float) * config.severity_scale
        if "actuator_delay" in config.enabled and "timestamp" in a:
            a["timestamp"] = pd.to_datetime(a["timestamp"]) + pd.to_timedelta(config.actuator_delay_steps, unit="s")
        return m, e, a
