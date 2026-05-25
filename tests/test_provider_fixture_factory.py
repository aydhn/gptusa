from usa_signal_bot.data_provider_runtime.provider_fixture_factory import sample_ohlcv_records, malformed_ohlcv_records_missing_close

def test_provider_fixture_factory():
    records = sample_ohlcv_records()
    assert len(records) == 5
    assert "close" in records[0]

    mal = malformed_ohlcv_records_missing_close()
    assert "close" not in mal[0]
