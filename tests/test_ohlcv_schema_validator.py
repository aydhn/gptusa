from usa_signal_bot.data_provider_runtime.ohlcv_schema_validator import validate_ohlcv_records
from usa_signal_bot.data_provider_runtime.provider_fixture_factory import sample_ohlcv_records, malformed_ohlcv_records_missing_close

def test_ohlcv_schema_validator():
    records = sample_ohlcv_records()
    errors = validate_ohlcv_records(records)
    assert len(errors) == 0

    mal = malformed_ohlcv_records_missing_close()
    errors2 = validate_ohlcv_records(mal)
    assert len(errors2) > 0
    assert "close" in errors2[0]
