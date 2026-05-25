
from usa_signal_bot.data_providers.provider_response_normalizer import normalize_provider_response
from usa_signal_bot.core.enums import DataProviderName, DataProviderCapability

def test_provider_response_normalizer():
    res = normalize_provider_response(DataProviderName.YFINANCE, {}, DataProviderCapability.GET_DAILY_OHLCV)
    assert isinstance(res, dict)
