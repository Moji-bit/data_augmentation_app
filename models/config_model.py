"""Configuration models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AugmentationConfig(BaseModel):
    jitter_std: float = 0.01
    scaling_min: float = 0.9
    scaling_max: float = 1.1
    drift_factor: float = 0.02
    noise_std: float = 0.005
    event_shift_steps: int = 1
    duration_scale: float = 1.1
    severity_scale: float = 1.1
    actuator_delay_steps: int = 1
    env_variation: float = 0.02
    traffic_variation: float = 0.05
    enabled: list[str] = Field(default_factory=lambda: ["jitter", "noise"])
