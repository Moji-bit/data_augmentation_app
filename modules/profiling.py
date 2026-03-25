"""Profiling module."""

from __future__ import annotations

from services.quality_service import QualityService


class ProfilingModule:
    def __init__(self) -> None:
        self.service = QualityService()
