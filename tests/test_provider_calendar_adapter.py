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

from unittest.mock import patch, MagicMock

def test_attach_calendar_metadata_no_data():
    cal = MagicMock()
    resp = MagicMock()
    resp.data = {}
    resp.metadata = {}

    from usa_signal_bot.calendar.provider_calendar_adapter import attach_calendar_metadata_to_provider_response
    result = attach_calendar_metadata_to_provider_response(resp, cal)
    assert "calendar_validation" not in result.metadata

def test_attach_calendar_metadata_with_data():
    cal = MagicMock()
    resp = MagicMock()
    resp.data = {"AAPL": [{"date": "2024-01-01"}]}
    resp.metadata = {}

    val_res = MagicMock()
    val_res.symbol = "AAPL"
    val_res.status.value = "VALID"
    val_res.missing_trading_days = 0
    val_res.non_trading_day_rows = 1
    val_res.early_close_rows = 0

    from usa_signal_bot.calendar.provider_calendar_adapter import attach_calendar_metadata_to_provider_response
    with patch('usa_signal_bot.calendar.provider_calendar_adapter.validate_provider_response_calendar_alignment') as mock_validate:
        mock_validate.return_value = [val_res]
        result = attach_calendar_metadata_to_provider_response(resp, cal)

    assert "calendar_validation" in result.metadata
    assert result.metadata["calendar_validation"]["AAPL"]["status"] == "VALID"
    assert result.metadata["calendar_validation"]["AAPL"]["missing_trading_days"] == 0
    assert result.metadata["calendar_validation"]["AAPL"]["non_trading_day_rows"] == 1
    assert result.metadata["calendar_validation"]["AAPL"]["early_close_rows"] == 0
