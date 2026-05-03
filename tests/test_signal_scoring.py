import pytest
from usa_signal_bot.core.config_schema import SignalScoringConfigSchema
from usa_signal_bot.core.exceptions import SignalScoringError
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket, SignalRiskFlag
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.signal_scoring import (
    default_signal_scoring_config,
    validate_signal_scoring_config,
    calculate_reason_quality_score,
    calculate_feature_snapshot_score,
    calculate_risk_penalty,
    clamp_score,
    calibrate_confidence_from_score,
    score_signal,
    score_signal_list
)

@pytest.fixture
def valid_config():
    return default_signal_scoring_config()

@pytest.fixture
def sample_signal():
    return StrategySignal(
        signal_id="TEST-123",
        strategy_name="TEST_STRAT",
        symbol="AAPL",
        timeframe="1d",
        timestamp_utc="2024-01-01T00:00:00Z",
        action=SignalAction.LONG,
        confidence=0.8,
        confidence_bucket=SignalConfidenceBucket.HIGH,
        score=0.0,
        reasons=["Price above SMA", "RSI is bullish"],
        feature_snapshot={"sma_50": 150.0, "rsi": 60.0},
        risk_flags=[]
    )

def test_default_config_is_valid():
    config = default_signal_scoring_config()
    validate_signal_scoring_config(config)

def test_invalid_config_raises_error():
    config = default_signal_scoring_config()
    config.min_score = -10.0
    with pytest.raises(SignalScoringError):
        validate_signal_scoring_config(config)

def test_calculate_reason_quality_score():
    assert calculate_reason_quality_score([]) == 0.0
    assert calculate_reason_quality_score(["Reason 1"]) == 0.4
    assert calculate_reason_quality_score(["Reason 1", "Reason 2"]) == 0.7
    assert calculate_reason_quality_score(["R1", "R2", "R3"]) == 0.9
    assert calculate_reason_quality_score(["R1", "R2", "R3", "R4"]) == 1.0

def test_calculate_feature_snapshot_score():
    assert calculate_feature_snapshot_score({}) == 0.0
    assert calculate_feature_snapshot_score({"a": 1}) == 0.4
    assert calculate_feature_snapshot_score({"a": 1, "b": 2, "c": 3}) == 0.7
    assert calculate_feature_snapshot_score({f"k{i}": i for i in range(10)}) == 0.9

def test_calculate_risk_penalty():
    assert calculate_risk_penalty([]) == 0.0
    assert calculate_risk_penalty([SignalRiskFlag.INSUFFICIENT_FEATURES]) > 0.0

def test_clamp_score():
    assert clamp_score(-10) == 0.0
    assert clamp_score(50) == 50.0
    assert clamp_score(150) == 100.0

def test_calibrate_confidence_from_score():
    assert calibrate_confidence_from_score(0) == 0.0
    assert calibrate_confidence_from_score(50) == 0.5
    assert calibrate_confidence_from_score(100) == 1.0
    assert calibrate_confidence_from_score(150) == 1.0

def test_score_signal_valid(sample_signal, valid_config):
    result = score_signal(sample_signal, valid_config)
    assert result.accepted_for_review is True
    assert result.scored_signal.score > 0
    assert result.breakdown.total_score == result.scored_signal.score
    assert len(result.errors) == 0

def test_score_signal_capped_without_backtest(sample_signal, valid_config):
    # Give a very strong signal
    sample_signal.reasons = ["R1", "R2", "R3", "R4", "R5"]
    sample_signal.feature_snapshot = {f"k{i}": i for i in range(20)}
    sample_signal.confidence = 1.0

    result = score_signal(sample_signal, valid_config)

    # Even with max everything, the score should not exceed max_allowed_score_without_backtest
    assert result.scored_signal.score <= valid_config.max_allowed_score_without_backtest
    assert "Score capped" in str(result.breakdown.notes)

def test_score_signal_list(sample_signal, valid_config):
    signals = [sample_signal, sample_signal]
    results = score_signal_list(signals, valid_config)
    assert len(results) == 2
