from pathlib import Path

import pandas as pd

from services.merge_service import MergeService


def test_build_master_empty(tmp_path: Path):
    svc = MergeService()
    out = svc.build_master([])
    assert out.empty
    assert "timestamp" in out.columns


def test_build_master_deduplicates(tmp_path: Path):
    p = tmp_path / "h.parquet"
    df = pd.DataFrame(
        {
            "timestamp": ["t1", "t1"],
            "scenario_id": ["s1", "s1"],
            "run_id": ["r1", "r1"],
            "labels": ["x", "x"],
        }
    )
    df.to_parquet(p, index=False)
    svc = MergeService()
    out = svc.build_master([p])
    assert len(out) == 1
