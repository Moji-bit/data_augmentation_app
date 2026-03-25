"""Project manager module."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from utils.constants import PROJECT_META_FILE


class ProjectManager:
    def create_or_load(self, name: str, owner: str) -> dict:
        PROJECT_META_FILE.parent.mkdir(parents=True, exist_ok=True)
        if PROJECT_META_FILE.exists():
            return json.loads(PROJECT_META_FILE.read_text(encoding="utf-8"))
        meta = {
            "project_name": name,
            "owner": owner,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "version": "v1",
        }
        PROJECT_META_FILE.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return meta

    def bump_version(self) -> dict:
        meta = json.loads(PROJECT_META_FILE.read_text(encoding="utf-8"))
        curr = int(meta["version"].replace("v", ""))
        meta["version"] = f"v{curr + 1}"
        PROJECT_META_FILE.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return meta
