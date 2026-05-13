"""Test provider calendar adapter."""
from usa_signal_bot.calendar.provider_calendar_adapter import attach_calendar_metadata_to_provider_response, provider_quality_with_calendar_adjustment
from usa_signal_bot.providers.provider_models import ProviderResponse, ProviderQualityScore
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar
from usa_signal_bot.core.enums import ProviderResponseStatus, ProviderQualityStatus, DataProviderName

def test_provider_calendar_adapter():
    cal = LocalMarketCalendar()
    resp = ProviderResponse("id", "req_id", DataProviderName.YFINANCE, ProviderResponseStatus.SUCCESS, "2024", 1, 2, {"SPY": [{"date": "2024-01-02"}, {"date": "2024-01-06"}]})

    resp_adj = attach_calendar_metadata_to_provider_response(resp, cal)
    assert "calendar_validation" in resp_adj.metadata

    score = ProviderQualityScore("id", "2024", DataProviderName.YFINANCE, ProviderQualityStatus.GOOD, 100.0, {})
    # For a real adjustment we would pass SessionValidationResults
    # Just asserting it's callable for now
    assert provider_quality_with_calendar_adjustment(score, []) == score
