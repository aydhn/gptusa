
from usa_signal_bot.data_providers.provider_selector import ProviderSelector
from usa_signal_bot.core.enums import DataProviderKind, DataProviderCapability, ProviderDataDomain

def test_provider_selector():
    selector = ProviderSelector()
    res = selector.select_provider(DataProviderKind.MARKET_DATA, DataProviderCapability.GET_DAILY_OHLCV, ProviderDataDomain.EQUITY_US)
    assert res.network_used is False
    assert res.broker_used is False
