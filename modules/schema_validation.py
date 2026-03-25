"""Schema validation module."""

from __future__ import annotations

from services.schema_service import SchemaService


class SchemaValidationModule:
    def __init__(self) -> None:
        self.service = SchemaService()
