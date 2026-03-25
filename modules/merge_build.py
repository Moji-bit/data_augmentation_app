"""Merge/build module."""

from __future__ import annotations

from services.merge_service import MergeService


class MergeBuildModule:
    def __init__(self) -> None:
        self.service = MergeService()
