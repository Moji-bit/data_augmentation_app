import pandas as pd

from services.schema_service import SchemaService


def test_validate_table_missing_columns():
    svc = SchemaService()
    df = pd.DataFrame({"timestamp": ["2026-01-01"]})
    res = svc.validate_table("events.csv", df)
    assert not res.valid
    assert any("missing columns" in issue for issue in res.issues)
