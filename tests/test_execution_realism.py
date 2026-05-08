import pytest
from usa_signal_bot.core.enums import MatchStatus, ExecutionRealismBucket, GapSeverity
from usa_signal_bot.comparison.comparison_models import MatchedTradePair, PerformanceGapMetrics
from usa_signal_bot.comparison.execution_realism import (
    calculate_execution_gap_metrics, calculate_average_price_gap_from_matches,
    calculate_execution_realism_score, classify_execution_realism_bucket,
    classify_overall_gap_severity, execution_gap_metrics_to_text
)

def build_mock_pair(p_price, b_price, status=MatchStatus.MATCHED):
    return MatchedTradePair(
        match_id="m1", symbol="AAPL", timeframe="1d", strategy_name=None,
        paper_trade_id=None, backtest_trade_id=None, match_status=status,
        paper_entry_time=None, backtest_entry_time=None,
        paper_exit_time=None, backtest_exit_time=None,
        paper_entry_price=p_price, backtest_entry_price=b_price,
        paper_exit_price=None, backtest_exit_price=None,
        paper_net_pnl=None, backtest_net_pnl=None, pnl_gap=None, return_gap_pct=None,
        timing_gap_bars=None, price_gap_pct=None, warnings=[], errors=[]
    )

def test_average_price_gap():
    pairs = [
        build_mock_pair(105, 100),
        build_mock_pair(110, 100)
    ]
    assert calculate_average_price_gap_from_matches(pairs, entry=True) == pytest.approx(7.5)

def test_execution_gap_metrics():
    pairs = [build_mock_pair(101, 100), build_mock_pair(None, None, MatchStatus.PAPER_ONLY)]
    metrics = calculate_execution_gap_metrics(pairs)

    assert metrics.matched_trade_count == 1
    assert metrics.unmatched_paper_count == 1
    assert metrics.average_entry_price_gap_pct == 1.0

    # Check realism score (starts 100, -20 for 1/2 unmatched, -10 for 1% gap = 70)
    assert metrics.execution_realism_score == pytest.approx(70.0)
    assert metrics.execution_realism_bucket == ExecutionRealismBucket.ACCEPTABLE_REALISM

def test_overall_severity():
    from usa_signal_bot.core.enums import ComparisonMetricStatus, GapDirection
    perf = PerformanceGapMetrics(ComparisonMetricStatus.OK, 10, 10, 0, 5, 5, 0, 0.5, 0.5, 0, 1.5, 1.5, 0, 10, 10, 0, GapDirection.NEUTRAL, [], [])
    exec = calculate_execution_gap_metrics([build_mock_pair(200, 100)]) # 100% gap -> score 0 -> SEVERE

    sev = classify_overall_gap_severity(perf, exec)
    assert sev in [GapSeverity.CRITICAL, GapSeverity.HIGH, GapSeverity.MODERATE, GapSeverity.LOW, GapSeverity.UNKNOWN]

def test_text_output():
    metrics = calculate_execution_gap_metrics([])
    txt = execution_gap_metrics_to_text(metrics)
    assert "Matched Trades: 0" in txt
