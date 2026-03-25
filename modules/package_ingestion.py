"""Package ingestion module."""

from __future__ import annotations

from pathlib import Path

from services.ingestion_service import IngestionService


class PackageIngestionModule:
    def __init__(self) -> None:
        self.service = IngestionService()

    def ingest(self, package_dir: Path) -> dict:
        return self.service.ingest_package(package_dir)
