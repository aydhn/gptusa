import pandas as pd
from usa_signal_bot.feature_engine.core_indicators.feature_table_builder import (
    build_core_feature_table, validate_feature_table, build_feature_table_schema
)

def test_feature_table_builder():
    records = []
    for i in range(50):
        records.append({
            "symbol": "AAPL",
            "timestamp": f"2023-01-{i%30+1:02d}T00:00:00Z",
            "open": 100 + i,
            "high": 105 + i,
            "low": 95 + i,
            "close": 102 + i,
            "adjusted_close": 102 + i,
            "volume": 1000 + i,
            "source": "test",
            "fetched_at_utc": "2023-01-01T00:00:00Z",
            "quality_flags": "[]"
        })

    df, res = build_core_feature_table(records)
    assert len(df) == 50
    assert "sma_20" in df.columns
