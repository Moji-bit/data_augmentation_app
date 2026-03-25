"""Export module."""

from __future__ import annotations

from services.export_service import ExportService


class ExportModule:
    export_parquet = staticmethod(ExportService.export_parquet)
