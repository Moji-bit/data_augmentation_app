"""Application constants."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STORAGE_DIR = PROJECT_ROOT / "storage"
RAW_DIR = STORAGE_DIR / "raw_packages"
PROCESSED_DIR = STORAGE_DIR / "processed"
HARMONIZED_DIR = STORAGE_DIR / "harmonized"
FINAL_DIR = STORAGE_DIR / "final"

REQUIRED_FILES = [
    "measurements_long.csv",
    "events.csv",
    "actuators.csv",
    "scenario.json",
]

EXPECTED_COLUMNS = {
    "measurements_long.csv": ["timestamp", "scenario_id", "tag", "value", "unit"],
    "events.csv": ["timestamp", "scenario_id", "event_type", "event_phase", "severity", "risk"],
    "actuators.csv": ["timestamp", "scenario_id", "actuator_tag", "value", "unit"],
}

MASTER_DATASET_NAME = "dataset_master.parquet"
REGISTRY_FILE = PROCESSED_DIR / "registry.csv"
PROJECT_META_FILE = STORAGE_DIR / "project_metadata.json"
