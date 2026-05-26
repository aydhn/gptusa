import pandas as pd
from usa_signal_bot.feature_engine.core_indicators.ohlcv_feature_input_loader import (
    records_to_dataframe, dataframe_to_records, validate_ohlcv_feature_input, sort_ohlcv_by_symbol_timestamp
)

def test_validate_ohlcv_feature_input_valid():
    records = [{
        "symbol": "AAPL", "timestamp": "2023-01-01T00:00:00Z",
        "open": 100.0, "high": 105.0, "low": 95.0, "close": 102.0,
        "adjusted_close": 102.0, "volume": 1000000, "source": "test",
        "fetched_at_utc": "2023-01-01T00:00:00Z", "quality_flags": "[]"
    }]
    errors = validate_ohlcv_feature_input(records)
    assert not errors
