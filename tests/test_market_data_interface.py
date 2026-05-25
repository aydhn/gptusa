
from usa_signal_bot.data_providers.interfaces.market_data import MarketDataProviderBase

def test_market_data():
    base = MarketDataProviderBase()
    req = base.build_daily_ohlcv_request("AAPL")
    assert req["symbol"] == "AAPL"
