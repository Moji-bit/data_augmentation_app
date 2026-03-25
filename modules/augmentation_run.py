"""Augmentation run module."""

from __future__ import annotations

from models.config_model import AugmentationConfig
from services.augmentation_service import AugmentationService


class AugmentationRunModule:
    def __init__(self) -> None:
        self.service = AugmentationService()

    def run(self, measurements, events, actuators, config: AugmentationConfig):
        return self.service.augment(measurements, events, actuators, config)
