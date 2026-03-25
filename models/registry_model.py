"""Registry row model."""

from __future__ import annotations

from pydantic import BaseModel


class RegistryRecord(BaseModel):
    package_id: str
    scenario_id: str
    run_id: str
    import_timestamp: str
    validation_status: str
    augmentation_status: str
    included_in_master_dataset: bool
    schema_version: str
