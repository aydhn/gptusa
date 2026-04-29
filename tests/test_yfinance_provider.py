import pytest
import pandas as pd
from datetime import datetime, timezone
from usa_signal_bot.data.yfinance_provider import YFinanceMarketDataProvider
from usa_signal_bot.data.models import MarketDataRequest
from usa_signal_bot.core.exceptions import DataProviderError

@pytest.fixture
def provider():
    return YFinanceMarketDataProvider()

def test_yfinance_provider_basic_properties(provider):
    assert provider.name == "yfinance"
    assert provider.capability.provider_name == "yfinance"
    assert provider.capability.free_only is True

def test_validate_request(provider):
    req = MarketDataRequest(symbols=["AAPL"], timeframe="1d", provider_name="yfinance")
    provider.validate_request(req) # Should not raise

    with pytest.raises(ValueError, match="Provider mismatch"):
        req_bad_name = MarketDataRequest(symbols=["AAPL"], timeframe="1d", provider_name="mock")
        provider.validate_request(req_bad_name)

    with pytest.raises(DataProviderError, match="Unsupported timeframe"):
        req_bad_tf = MarketDataRequest(symbols=["AAPL"], timeframe="invalid", provider_name="yfinance")
        provider.validate_request(req_bad_tf)

def test_build_fetch_plan(provider):
    req = MarketDataRequest(symbols=["AAPL", "MSFT", "GOOGL"], timeframe="1d", provider_name="yfinance")
    provider.policy.rate_limit.max_symbols_per_batch = 2
    plan = provider.build_fetch_plan(req)
    assert plan.provider_name == "yfinance"
    assert plan.batch_count == 2
    assert plan.estimated_requests == 2

def test_check_status(provider):
    status = provider.check_status()
    assert status.available is True
    assert "yfinance" in status.message

def test_fetch_ohlcv_mocked_yfinance(monkeypatch, provider):
    def mock_download(*args, **kwargs):
        # Create a fake df that normalizer will accept
        cols = pd.MultiIndex.from_tuples([
            ("Open", "AAPL"), ("High", "AAPL"), ("Low", "AAPL"), ("Close", "AAPL"), ("Volume", "AAPL")
        ])
        df = pd.DataFrame([[100, 105, 95, 101, 1000]], columns=cols, index=[pd.Timestamp("2023-01-01")])
        return df

    monkeypatch.setattr("yfinance.download", mock_download)

    req = MarketDataRequest(symbols=["AAPL"], timeframe="1d", provider_name="yfinance")
    resp = provider.fetch_ohlcv(req)
    assert resp.success is True
    assert len(resp.errors) == 0
    assert len(resp.bars) == 1
    assert resp.bars[0].symbol == "AAPL"

def test_fetch_ohlcv_empty_dataframe(monkeypatch, provider):
    def mock_download(*args, **kwargs):
        return pd.DataFrame()

    monkeypatch.setattr("yfinance.download", mock_download)

    req = MarketDataRequest(symbols=["AAPL"], timeframe="1d", provider_name="yfinance")
    resp = provider.fetch_ohlcv(req)
    assert resp.success is False
    assert len(resp.warnings) == 1
    assert "No data returned" in resp.warnings[0]
    assert len(resp.bars) == 0

def test_fetch_ohlcv_exception(monkeypatch, provider):
    def mock_download(*args, **kwargs):
        raise ValueError("Network error")

    monkeypatch.setattr("yfinance.download", mock_download)

    req = MarketDataRequest(symbols=["AAPL"], timeframe="1d", provider_name="yfinance")
    resp = provider.fetch_ohlcv(req)
    assert resp.success is False
    assert len(resp.errors) == 1
    assert "Network error" in resp.errors[0]
