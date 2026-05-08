import pytest
from usa_signal_bot.core.enums import MatchStatus, ComparisonMetricStatus, GapSeverity
from usa_signal_bot.comparison.comparison_models import MatchedTradePair
from usa_signal_bot.comparison.timing_gap import (
    calculate_timing_gap_metrics, estimate_timing_gap_bars,
    classify_timing_gap_severity, timing_gap_metrics_to_text
)

def test_estimate_timing_gap_bars():
    assert estimate_timing_gap_bars("2023-01-05T10:00:00", "2023-01-01T10:00:00") == 4
    assert estimate_timing_gap_bars("2023-01-15T00:00:00", "2023-01-01T00:00:00", "1w") == 2
    assert estimate_timing_gap_bars(None, "2023-01-01T10:00:00") is None

def test_timing_gap_metrics():
    pairs = [
        MatchedTradePair(
            match_id="m1", symbol="AAPL", timeframe="1d", strategy_name=None,
            paper_trade_id=None, backtest_trade_id=None, match_status=MatchStatus.MATCHED,
            paper_entry_time="2023-01-05T00:00:00", backtest_entry_time="2023-01-01T00:00:00",
            paper_exit_time="2023-01-10T00:00:00", backtest_exit_time="2023-01-10T00:00:00",
            paper_entry_price=None, backtest_entry_price=None, paper_exit_price=None, backtest_exit_price=None,
            paper_net_pnl=None, backtest_net_pnl=None, pnl_gap=None, return_gap_pct=None,
            timing_gap_bars=None, price_gap_pct=None, warnings=[], errors=[]
        )
    ]

    res = calculate_timing_gap_metrics(pairs)
    assert res.status == ComparisonMetricStatus.OK
    assert res.matched_count == 1
    assert res.average_entry_timing_gap_bars == 4.0
    assert res.average_exit_timing_gap_bars == 0.0
    assert res.delayed_entry_count == 1
    assert res.delayed_exit_count == 0

def test_severity_classification():
    pairs = [
        MatchedTradePair(
            match_id="m1", symbol="AAPL", timeframe="1d", strategy_name=None,
            paper_trade_id=None, backtest_trade_id=None, match_status=MatchStatus.MATCHED,
            paper_entry_time="2023-01-10T00:00:00", backtest_entry_time="2023-01-01T00:00:00",
            paper_exit_time=None, backtest_exit_time=None,
            paper_entry_price=None, backtest_entry_price=None, paper_exit_price=None, backtest_exit_price=None,
            paper_net_pnl=None, backtest_net_pnl=None, pnl_gap=None, return_gap_pct=None,
            timing_gap_bars=None, price_gap_pct=None, warnings=[], errors=[]
        )
    ]
    res = calculate_timing_gap_metrics(pairs)
    sev = classify_timing_gap_severity(res)
    assert sev == GapSeverity.CRITICAL

def test_text_output():
    res = calculate_timing_gap_metrics([])
    txt = timing_gap_metrics_to_text(res)
    assert "Matched Trades: 0" in txt
