"""Augmentation config module."""

from __future__ import annotations

from models.config_model import AugmentationConfig


class AugmentationConfigModule:
    def default(self) -> AugmentationConfig:
        return AugmentationConfig()
