import pytest
from usa_signal_bot.core.enums import ComparisonStatus, ComparisonReportType, MatchStatus, ComparisonMetricStatus, ExecutionRealismBucket, SignalDriftStatus, GapSeverity, GapDirection, ComparisonSourceType
from usa_signal_bot.comparison.comparison_models import (
    ComparisonRunRequest, ComparisonSourceSummary, MatchedTradePair,
    PerformanceGapMetrics, ExecutionGapMetrics, SignalDriftMetrics,
    ComparisonRunResult, create_comparison_request_id, create_comparison_run_id,
    create_trade_match_id, validate_comparison_run_request, validate_matched_trade_pair,
    validate_comparison_run_result, comparison_run_result_to_dict
)

def test_comparison_run_request_creation():
    req = ComparisonRunRequest(
        request_id="test1",
        report_type=ComparisonReportType.FULL_COMPARISON,
        paper_run_id="p1",
        backtest_run_id="b1"
    )
    assert req.request_id == "test1"
    validate_comparison_run_request(req)

def test_comparison_run_request_invalid():
    with pytest.raises(ValueError, match="request_id cannot be empty"):
        validate_comparison_run_request(ComparisonRunRequest(request_id="", report_type=ComparisonReportType.FULL_COMPARISON))

    with pytest.raises(ValueError, match="Must provide at least one paper/signal source"):
        validate_comparison_run_request(ComparisonRunRequest(request_id="123", report_type=ComparisonReportType.FULL_COMPARISON))

def test_source_summary():
    s = ComparisonSourceSummary(
        source_type=ComparisonSourceType.PAPER_RUN,
        source_id="p1",
        source_path="data/p1",
        record_count=10,
        symbols=["AAPL"],
        timeframes=["1d"],
        warnings=[],
        errors=[]
    )
    assert s.source_type == ComparisonSourceType.PAPER_RUN

def test_matched_trade_pair():
    p = MatchedTradePair(
        match_id="m1",
        symbol="AAPL",
        timeframe="1d",
        strategy_name=None,
        paper_trade_id="pt1",
        backtest_trade_id="bt1",
        match_status=MatchStatus.MATCHED,
        paper_entry_time=None, backtest_entry_time=None,
        paper_exit_time=None, backtest_exit_time=None,
        paper_entry_price=100.0, backtest_entry_price=99.0,
        paper_exit_price=110.0, backtest_exit_price=109.0,
        paper_net_pnl=10.0, backtest_net_pnl=10.0,
        pnl_gap=0.0, return_gap_pct=0.0, timing_gap_bars=0,
        price_gap_pct=1.0, warnings=[], errors=[]
    )
    validate_matched_trade_pair(p)

def test_metrics_models():
    p_gap = PerformanceGapMetrics(ComparisonMetricStatus.OK, 10, 10, 0, 5, 5, 0, 0.5, 0.5, 0, 1.5, 1.5, 0, 10, 10, 0, GapDirection.NEUTRAL, [], [])
    e_gap = ExecutionGapMetrics(ComparisonMetricStatus.OK, 10, 0, 0, 0.1, 0.1, 0, 0, 0, 0, 0, 95.0, ExecutionRealismBucket.HIGH_REALISM, [], [])
    s_drift = SignalDriftMetrics(ComparisonMetricStatus.OK, 10, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, SignalDriftStatus.NO_DRIFT, [], [])

    assert p_gap.status == ComparisonMetricStatus.OK

def test_comparison_result():
    res = ComparisonRunResult(
        run_id="run1",
        created_at_utc="2023-01-01T00:00:00Z",
        status=ComparisonStatus.COMPLETED,
        request=ComparisonRunRequest("req1", ComparisonReportType.FULL_COMPARISON, paper_run_id="p1", backtest_run_id="b1"),
        paper_source=None, backtest_source=None, scan_source=None,
        matched_trades=[],
        performance_gap=PerformanceGapMetrics(ComparisonMetricStatus.OK, 10, 10, 0, 5, 5, 0, 0.5, 0.5, 0, 1.5, 1.5, 0, 10, 10, 0, GapDirection.NEUTRAL, [], []),
        execution_gap=ExecutionGapMetrics(ComparisonMetricStatus.OK, 10, 0, 0, 0.1, 0.1, 0, 0, 0, 0, 0, 95.0, ExecutionRealismBucket.HIGH_REALISM, [], []),
        signal_drift=None,
        execution_realism_bucket=ExecutionRealismBucket.HIGH_REALISM,
        overall_gap_severity=GapSeverity.LOW,
        output_paths={}, warnings=[], errors=[]
    )
    validate_comparison_run_result(res)
    d = comparison_run_result_to_dict(res)
    assert d["run_id"] == "run1"

def test_id_factories():
    assert create_comparison_request_id().startswith("comparison_req_")
    assert create_comparison_run_id().startswith("comparison_")
    assert create_trade_match_id("AAPL", "pt1", "bt1").startswith("match_AAPL_pt1_bt1_")
