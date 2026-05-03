import pytest
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket
from usa_signal_bot.strategies.signal_contract import StrategySignal, validate_strategy_signal, confidence_to_bucket, signal_to_dict, signal_to_text, create_watch_signal, create_signal_id
from usa_signal_bot.core.exceptions import SignalContractError

def test_signal_contract_valid():
    sig = StrategySignal(
        signal_id="123",
        strategy_name="test",
        symbol="AAPL",
        timeframe="1d",
        timestamp_utc="2023-01-01T00:00:00Z",
        action=SignalAction.WATCH,
        confidence=0.5,
        confidence_bucket=SignalConfidenceBucket.MODERATE,
        score=50.0,
        reasons=["reason1"],
        feature_snapshot={"f1": 1},
        risk_flags=[]
    )
    validate_strategy_signal(sig) # should not raise

def test_signal_contract_invalid_confidence():
    sig = StrategySignal(
        signal_id="123",
        strategy_name="test",
        symbol="AAPL",
        timeframe="1d",
        timestamp_utc="2023-01-01T00:00:00Z",
        action=SignalAction.WATCH,
        confidence=1.5,
        confidence_bucket=SignalConfidenceBucket.MODERATE,
        score=50.0,
        reasons=["reason1"],
        feature_snapshot={},
        risk_flags=[]
    )
    with pytest.raises(SignalContractError):
        validate_strategy_signal(sig)

def test_signal_utils():
    assert confidence_to_bucket(0.9) == SignalConfidenceBucket.VERY_HIGH

    sig = create_watch_signal("test", "AAPL", "1d", "2023-01-01T00:00:00Z", "test reason", 0.6)
    assert sig.action == SignalAction.WATCH
    assert sig.confidence == 0.6

    d = signal_to_dict(sig)
    assert d["strategy_name"] == "test"

    t = signal_to_text(sig)
    assert "AAPL" in t

    id1 = create_signal_id("test", "AAPL", "1d", "ts1")
    id2 = create_signal_id("test", "AAPL", "1d", "ts1")
    assert id1 == id2
    assert len(id1) > 0

def test_signal_contract_new_fields():
    sample_signal = StrategySignal(signal_id='test', strategy_name='test', symbol='AAPL', timeframe='1d', timestamp_utc='2024-01-01T00:00:00Z', action=SignalAction.LONG, confidence=0.8, confidence_bucket=SignalConfidenceBucket.HIGH, score=80.0, reasons=['test'], feature_snapshot={}, risk_flags=[])
    from usa_signal_bot.core.enums import SignalQualityStatus, ConfluenceDirection

    sample_signal.quality_status = SignalQualityStatus.ACCEPTED
    sample_signal.score_breakdown = {"base": 50, "bonus": 10}
    sample_signal.confluence_score = 80.0
    sample_signal.confluence_direction = ConfluenceDirection.LONG_BIAS

    validate_strategy_signal(sample_signal)

    d = signal_to_dict(sample_signal)
    assert d["quality_status"] == "ACCEPTED"
    assert d["score_breakdown"] == {"base": 50, "bonus": 10}
    assert d["confluence_score"] == 80.0
    assert d["confluence_direction"] == "LONG_BIAS"

def test_signal_contract_invalid_confluence_score():
    sample_signal = StrategySignal(signal_id='test', strategy_name='test', symbol='AAPL', timeframe='1d', timestamp_utc='2024-01-01T00:00:00Z', action=SignalAction.LONG, confidence=0.8, confidence_bucket=SignalConfidenceBucket.HIGH, score=80.0, reasons=['test'], feature_snapshot={}, risk_flags=[])
    sample_signal.confluence_score = 150.0
    with pytest.raises(SignalContractError):
        validate_strategy_signal(sample_signal)
