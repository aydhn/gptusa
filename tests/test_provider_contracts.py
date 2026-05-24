import pytest
from usa_signal_bot.advanced_runtime.provider_contracts import build_provider_data_request
from usa_signal_bot.core.enums import ProviderInterfaceKind, ProviderCapability

def test_build_request():
    req = build_provider_data_request("test", ProviderInterfaceKind.MARKET_DATA, ProviderCapability.GET_DAILY_BARS)
    assert req.provider_name == "test"
    assert req.metadata_only is True
