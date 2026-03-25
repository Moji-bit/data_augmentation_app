"""Scenario metadata model."""

from __future__ import annotations

from pydantic import BaseModel


class ScenarioModel(BaseModel):
    scenario_id: str
    description: str | None = None
    location: str | None = None
    schema_version: str = "1.0"
