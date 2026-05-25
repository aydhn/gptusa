from usa_signal_bot.data_providers.adapters.local_csv_adapter import LocalCsvMarketDataAdapter

def test_local_csv_adapter():
    adapter = LocalCsvMarketDataAdapter()
    spec = adapter.adapter_spec()
    assert spec["provider_name"] == "LOCAL_CSV"

    # testing missing path
    res = adapter.read_local_fixture("does_not_exist.csv")
    assert "error" in res
