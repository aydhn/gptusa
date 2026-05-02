import pytest
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.signal_validation import validate_signal_list, assert_signals_valid
from usa_signal_bot.core.exceptions import SignalValidationError

def make_sig(sig_id, conf=0.5):
    return StrategySignal(
        signal_id=sig_id,
        strategy_name="test",
        symbol="AAPL",
        timeframe="1d",
        timestamp_utc="2023-01-01T00:00:00Z",
        action=SignalAction.WATCH,
        confidence=conf,
        confidence_bucket=SignalConfidenceBucket.MODERATE,
        score=conf*100,
        reasons=["r1"],
        feature_snapshot={},
        risk_flags=[]
    )

def test_signal_validation_valid():
    sigs = [make_sig("1"), make_sig("2")]
    rep = validate_signal_list(sigs)
    assert rep.valid
    assert rep.total_signals == 2
    assert_signals_valid(rep) # should not raise

def test_signal_validation_duplicates():
    sigs = [make_sig("1"), make_sig("1")]
    rep = validate_signal_list(sigs)
    assert not rep.valid
    assert rep.invalid_signals > 0
    with pytest.raises(SignalValidationError):
        assert_signals_valid(rep)

def test_signal_validation_overconfidence():
    sigs = [make_sig(str(i), conf=0.9) for i in range(10)]
    rep = validate_signal_list(sigs)
    assert rep.valid # overconfidence is a warning, not an error
    assert len(rep.warnings) > 0

def test_signal_validation_empty():
    rep = validate_signal_list([])
    assert rep.valid
    assert len(rep.warnings) > 0
