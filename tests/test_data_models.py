import pytest
from usa_signal_bot.data.models import MarketDataRequest, MarketDataResponse, ProviderFetchPlan, ProviderStatus, OHLCVBar

def test_market_data_request_valid():
    req = MarketDataRequest(symbols=["AAPL"], timeframe="1d", provider_name="mock")
    assert req.symbols == ["AAPL"]

def test_market_data_request_empty_symbols_fails():
    with pytest.raises(ValueError):
        MarketDataRequest(symbols=[], timeframe="1d", provider_name="mock")

def test_market_data_response_methods():
    req = MarketDataRequest(symbols=["AAPL", "MSFT"], timeframe="1d", provider_name="mock")
    bars = [
        OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc="2023-01-01T00:00:00Z", open=1, high=2, low=1, close=1.5, volume=100),
        OHLCVBar(symbol="MSFT", timeframe="1d", timestamp_utc="2023-01-01T00:00:00Z", open=1, high=2, low=1, close=1.5, volume=100)
    ]
    resp = MarketDataResponse(request=req, provider_name="mock", bars=bars, success=True)

    assert resp.bar_count() == 2
    assert set(resp.symbols_returned()) == {"AAPL", "MSFT"}
    assert resp.has_errors() is False

def test_provider_fetch_plan_serializes():
    plan = ProviderFetchPlan(provider_name="mock", symbols=["AAPL"], timeframe="1d", batch_count=1, estimated_requests=1)
    d = plan.to_dict()
    assert d["provider_name"] == "mock"
    assert d["batch_count"] == 1

def test_provider_status_serializes():
    status = ProviderStatus(provider_name="mock", available=True, message="OK")
    d = status.to_dict()
    assert d["provider_name"] == "mock"
    assert d["available"] is True
