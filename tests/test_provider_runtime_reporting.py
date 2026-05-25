from usa_signal_bot.data_provider_runtime.provider_runtime_reporting import provider_runtime_limitations_text

def test_provider_runtime_reporting():
    t = provider_runtime_limitations_text()
    assert "NOT an active paper trading environment" in t
