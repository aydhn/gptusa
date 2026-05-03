import pytest
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket, SignalAggregationMode, ConfluenceDirection, ConfluenceStrength
from usa_signal_bot.core.config_schema import ConfluenceConfig
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.signal_confluence import (
    group_signals_for_confluence,
    detect_conflicting_signals,
    classify_confluence_direction,
    calculate_confluence_score,
    classify_confluence_strength,
    evaluate_confluence_group,
    evaluate_confluence,
    confluence_report_to_text
)

@pytest.fixture
def default_config():
    return ConfluenceConfig()

@pytest.fixture
def sample_signals():
    s1 = StrategySignal(
        signal_id="TEST-1", strategy_name="S1", symbol="AAPL", timeframe="1d",
        timestamp_utc="2024-01-01T00:00:00Z", action=SignalAction.LONG,
        confidence=0.8, confidence_bucket=SignalConfidenceBucket.HIGH,
        score=60.0, reasons=[], feature_snapshot={}, risk_flags=[]
    )
    s2 = StrategySignal(
        signal_id="TEST-2", strategy_name="S2", symbol="AAPL", timeframe="1d",
        timestamp_utc="2024-01-01T00:00:00Z", action=SignalAction.LONG,
        confidence=0.7, confidence_bucket=SignalConfidenceBucket.HIGH,
        score=55.0, reasons=[], feature_snapshot={}, risk_flags=[]
    )
    s3 = StrategySignal(
        signal_id="TEST-3", strategy_name="S3", symbol="MSFT", timeframe="1d",
        timestamp_utc="2024-01-01T00:00:00Z", action=SignalAction.SHORT,
        confidence=0.9, confidence_bucket=SignalConfidenceBucket.VERY_HIGH,
        score=80.0, reasons=[], feature_snapshot={}, risk_flags=[]
    )
    return [s1, s2, s3]

def test_group_signals_for_confluence(sample_signals):
    groups = group_signals_for_confluence(sample_signals, SignalAggregationMode.BY_SYMBOL_TIMEFRAME)
    assert len(groups) == 2
    assert len(groups["AAPL_1d"]) == 2
    assert len(groups["MSFT_1d"]) == 1

def test_detect_conflicting_signals(sample_signals):
    assert detect_conflicting_signals(sample_signals[:2]) is False
    assert detect_conflicting_signals(sample_signals) is True

def test_classify_confluence_direction(sample_signals):
    assert classify_confluence_direction(sample_signals[:2]) == ConfluenceDirection.LONG_BIAS
    assert classify_confluence_direction(sample_signals) == ConfluenceDirection.CONFLICTED

def test_calculate_confluence_score(sample_signals, default_config):
    score = calculate_confluence_score(sample_signals[:2], default_config)
    assert 0.0 < score <= 100.0

    conflict_score = calculate_confluence_score(sample_signals, default_config)
    assert conflict_score <= 25.0  # 50 - 25 penalty

def test_classify_confluence_strength(default_config):
    assert classify_confluence_strength(80.0, 2, default_config) == ConfluenceStrength.STRONG
    assert classify_confluence_strength(80.0, 1, default_config) == ConfluenceStrength.NONE # Not enough signals

def test_evaluate_confluence_group(sample_signals, default_config):
    res = evaluate_confluence_group(sample_signals[:2], default_config)
    assert res.symbol == "AAPL"
    assert res.direction == ConfluenceDirection.LONG_BIAS
    assert res.conflicting is False
    assert res.signal_count == 2

def test_evaluate_confluence(sample_signals, default_config):
    report = evaluate_confluence(sample_signals, config=default_config)
    assert report.total_groups == 1  # Only AAPL has >= 2 signals
    assert report.conflicted_groups == 0
    assert "AAPL" in report.group_results[0].symbol

def test_confluence_report_to_text(sample_signals, default_config):
    report = evaluate_confluence(sample_signals, config=default_config)
    text = confluence_report_to_text(report)
    assert "Total Groups Evaluated: 1" in text
    assert "AAPL" in text
