import pandas as pd

from services.harmonization_service import HarmonizationService


def test_build_harmonized_contains_required_flags():
    svc = HarmonizationService()
    m = pd.DataFrame(
        {
            "timestamp": ["2026-01-01T00:00:00Z"],
            "scenario_id": ["s1"],
            "tag": ["S1"],
            "value": [1.0],
            "unit": ["C"],
        }
    )
    e = pd.DataFrame(
        {
            "timestamp": ["2026-01-01T00:00:00Z"],
            "scenario_id": ["s1"],
            "event_type": ["alarm"],
            "event_phase": ["rise"],
            "severity": [0.5],
            "risk": ["medium"],
        }
    )
    a = pd.DataFrame(
        {
            "timestamp": ["2026-01-01T00:00:00Z"],
            "scenario_id": ["s1"],
            "actuator_tag": ["A1"],
            "value": [0.2],
            "unit": ["ratio"],
        }
    )
    out = svc.build_harmonized(m, e, a, {"scenario_id": "s1"}, run_id="r1", is_augmented=True)
    assert "sensor_features" in out
    assert bool(out["is_augmented"].iloc[0]) is True
