import pytest
from usa_signal_bot.advanced_runtime.provider_capability_manifest import default_market_data_provider_manifest

def test_manifest():
    m = default_market_data_provider_manifest("test")
    assert m.provider_name == "test"
