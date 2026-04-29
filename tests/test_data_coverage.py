import pytest
from pathlib import Path
from usa_signal_bot.data.coverage import (
    calculate_expected_min_bars, calculate_symbol_timeframe_coverage,
    calculate_coverage_report, has_minimum_coverage, coverage_report_to_text,
    write_coverage_report_json
)
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.core.enums import DataCoverageStatus

def test_calculate_expected_min_bars():
    assert calculate_expected_min_bars("1d", 30) > 0
    assert calculate_expected_min_bars("1h", 1) > 0
    assert calculate_expected_min_bars("15m", 1) > 0

def test_calculate_symbol_timeframe_coverage_empty():
    cov = calculate_symbol_timeframe_coverage("AAPL", "1d", [], 20)
    assert cov.status == DataCoverageStatus.EMPTY
    assert cov.coverage_ratio == 0.0

def test_calculate_symbol_timeframe_coverage_ready():
    bars = [OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc=f"2023-01-{i:02d}T00:00:00Z", open=100.0, high=105.0, low=95.0, close=102.0, volume=1000) for i in range(1, 21)]
    cov = calculate_symbol_timeframe_coverage("AAPL", "1d", bars, 20)
    assert cov.status == DataCoverageStatus.COMPLETE
    assert cov.coverage_ratio == 1.0

def test_calculate_symbol_timeframe_coverage_partial():
    bars = [OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc=f"2023-01-{i:02d}T00:00:00Z", open=100.0, high=105.0, low=95.0, close=102.0, volume=1000) for i in range(1, 15)]
    cov = calculate_symbol_timeframe_coverage("AAPL", "1d", bars, 20)
    assert cov.status == DataCoverageStatus.PARTIAL

def test_calculate_symbol_timeframe_coverage_stale():
    bars = [OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc=f"2020-01-{i:02d}T00:00:00Z", open=100.0, high=105.0, low=95.0, close=102.0, volume=1000) for i in range(1, 21)]
    cov = calculate_symbol_timeframe_coverage("AAPL", "1d", bars, 20, stale_after_seconds=86400)
    assert cov.stale is True
    assert cov.status == DataCoverageStatus.STALE

def test_coverage_report_logic():
    bars = [OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc=f"2023-01-{i:02d}T00:00:00Z", open=100.0, high=105.0, low=95.0, close=102.0, volume=1000) for i in range(1, 21)]
    report = calculate_coverage_report("yfinance", ["AAPL", "MSFT"], ["1d"], {"1d": bars})

    assert report.total_symbol_timeframe_pairs == 2
    assert report.ready_pairs == 1  # AAPL
    assert report.empty_pairs == 1  # MSFT
    assert report.status == DataCoverageStatus.PARTIAL

def test_has_minimum_coverage():
    bars = [OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc=f"2023-01-{i:02d}T00:00:00Z", open=100.0, high=105.0, low=95.0, close=102.0, volume=1000) for i in range(1, 21)]
    report = calculate_coverage_report("yfinance", ["AAPL", "MSFT"], ["1d"], {"1d": bars})

    # AAPL is ready (1/2 = 0.5)
    assert has_minimum_coverage(report, 0.4) is True
    assert has_minimum_coverage(report, 0.6) is False

def test_coverage_report_to_text():
    bars = [OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc=f"2023-01-01T00:00:00Z", open=100.0, high=105.0, low=95.0, close=102.0, volume=1000)]
    report = calculate_coverage_report("yfinance", ["AAPL"], ["1d"], {"1d": bars})
    text = coverage_report_to_text(report)
    assert "Provider: yfinance" in text
    assert "AAPL" in text

def test_write_coverage_report_json(tmp_path):
    bars = [OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc=f"2023-01-01T00:00:00Z", open=100.0, high=105.0, low=95.0, close=102.0, volume=1000)]
    report = calculate_coverage_report("yfinance", ["AAPL"], ["1d"], {"1d": bars})
    p = tmp_path / "report.json"
    write_coverage_report_json(p, report)
    assert p.exists()
    import json
    with open(p) as f:
        data = json.load(f)
        assert data["provider_name"] == "yfinance"
