import pytest
from usa_signal_bot.data.readiness import (
    DataReadinessReport,
    DataReadinessItem,
    DataReadinessStatus,
    readiness_items_by_symbol,
    symbol_readiness_score,
    symbol_ready_timeframes,
    symbol_missing_or_failed_timeframes
)

def test_readiness_helpers():
    report = DataReadinessReport(
        report_id="1",
        items=[
            DataReadinessItem(symbol="AAPL", timeframe="1d", status=DataReadinessStatus.READY),
            DataReadinessItem(symbol="AAPL", timeframe="1h", status=DataReadinessStatus.NOT_READY),
            DataReadinessItem(symbol="AAPL", timeframe="15m", status=DataReadinessStatus.FAILED),
            DataReadinessItem(symbol="MSFT", timeframe="1d", status=DataReadinessStatus.READY),
        ]
    )

    by_sym = readiness_items_by_symbol(report)
    assert "AAPL" in by_sym
    assert len(by_sym["AAPL"]) == 3

    score = symbol_readiness_score(report, "AAPL")
    assert pytest.approx(score, 0.1) == 33.33

    ready = symbol_ready_timeframes(report, "AAPL")
    assert ready == ["1d"]

    missing, failed = symbol_missing_or_failed_timeframes(report, "AAPL")
    assert missing == ["1h"]
    assert failed == ["15m"]
