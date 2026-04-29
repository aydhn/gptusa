import pytest
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.data.quality import (
    DataQualityIssue, DataQualityReport, validate_ohlcv_bar_quality,
    validate_ohlcv_bars_quality, data_quality_report_to_text, assert_data_quality_acceptable
)
from usa_signal_bot.core.enums import DataQualityStatus
from usa_signal_bot.core.exceptions import DataValidationError

def test_validate_ohlcv_bar_quality_ok():
    # Correct OHLCVBar initialization with keyword args to avoid strict positional issues
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=101.0, volume=1000.0)
    issues = validate_ohlcv_bar_quality(bar)
    assert len(issues) == 0

def test_validate_ohlcv_bar_quality_high_low():
    # Bypass initial validation via __new__ to test the specific quality check
    bar = OHLCVBar.__new__(OHLCVBar)
    bar.symbol = "AAPL"
    bar.timestamp_utc = "2023-01-01T00:00:00Z"
    bar.timeframe = "1d"
    bar.open = 100.0
    bar.high = 90.0
    bar.low = 95.0
    bar.close = 101.0
    bar.volume = 1000.0

    issues = validate_ohlcv_bar_quality(bar)
    assert len(issues) == 1
    assert issues[0].field == "high/low"
    assert issues[0].severity == "ERROR"

def test_validate_ohlcv_bar_quality_negative_volume():
    # Bypass initial validation via __new__ to test the specific quality check
    bar = OHLCVBar.__new__(OHLCVBar)
    bar.symbol = "AAPL"
    bar.timestamp_utc = "2023-01-01T00:00:00Z"
    bar.timeframe = "1d"
    bar.open = 100.0
    bar.high = 105.0
    bar.low = 95.0
    bar.close = 101.0
    bar.volume = -1.0

    issues = validate_ohlcv_bar_quality(bar)
    assert len(issues) == 1
    assert issues[0].field == "volume"

def test_validate_ohlcv_bars_quality_missing_symbol():
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=101.0, volume=1000.0)
    report = validate_ohlcv_bars_quality([bar], ["AAPL", "MSFT"], "yfinance", "1d")
    assert report.total_bars == 1
    assert "MSFT" in report.missing_symbols
    assert report.status == DataQualityStatus.WARNING

def test_validate_ohlcv_bars_quality_empty():
    report = validate_ohlcv_bars_quality([], ["AAPL"], "yfinance", "1d")
    assert report.status == DataQualityStatus.ERROR
    assert report.total_bars == 0

def test_validate_ohlcv_bars_quality_duplicate():
    bar1 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=101.0, volume=1000.0)
    bar2 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=105.0, low=95.0, close=101.0, volume=1000.0)
    report = validate_ohlcv_bars_quality([bar1, bar2], ["AAPL"], "yfinance", "1d")
    assert report.status == DataQualityStatus.WARNING
    assert any("Duplicate" in i.message for i in report.issues)

def test_assert_data_quality_acceptable():
    report = DataQualityReport(status=DataQualityStatus.OK)
    assert_data_quality_acceptable(report) # Should not raise

    report.status = DataQualityStatus.ERROR
    with pytest.raises(DataValidationError):
        assert_data_quality_acceptable(report)

    report.status = DataQualityStatus.WARNING
    assert_data_quality_acceptable(report, allow_warnings=True) # Should not raise
    with pytest.raises(DataValidationError):
        assert_data_quality_acceptable(report, allow_warnings=False)
