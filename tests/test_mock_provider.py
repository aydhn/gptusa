import pytest
from usa_signal_bot.data.mock_provider import MockMarketDataProvider
from usa_signal_bot.data.models import MarketDataRequest, OHLCVBar

def test_mock_status_is_available():
    provider = MockMarketDataProvider()
    status = provider.check_status()
    assert status.available is True

def test_mock_build_fetch_plan():
    provider = MockMarketDataProvider()
    req = MarketDataRequest(symbols=["AAPL", "MSFT", "GOOGL"], timeframe="1d", provider_name="mock")
    # By default, mock provider policy max_symbols_per_batch is 50
    plan = provider.build_fetch_plan(req)
    assert plan.batch_count == 1
    assert len(plan.symbols) == 3

def test_mock_fetch_ohlcv():
    provider = MockMarketDataProvider()
    req = MarketDataRequest(symbols=["AAPL", "MSFT"], timeframe="1d", provider_name="mock")
    resp = provider.fetch_ohlcv(req)

    assert resp.success is True
    assert resp.bar_count() == 2
    assert not resp.from_cache

    symbols_returned = resp.symbols_returned()
    assert "AAPL" in symbols_returned
    assert "MSFT" in symbols_returned

    for bar in resp.bars:
        assert isinstance(bar, OHLCVBar)
        assert bar.open > 0
        assert bar.volume > 0
        assert bar.source == "mock"
