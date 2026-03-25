"""Harmonization module."""

from __future__ import annotations

from services.harmonization_service import HarmonizationService


class HarmonizationModule:
    def __init__(self) -> None:
        self.service = HarmonizationService()
