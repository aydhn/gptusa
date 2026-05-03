import pytest
from usa_signal_bot.core.enums import SignalRiskFlag, SignalAction, SignalConfidenceBucket
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.signal_risk_flags import (
    assign_risk_flags,
    merge_risk_flags,
    risk_flags_to_text,
    has_high_risk_flags
)

@pytest.fixture
def empty_signal():
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
        reasons=[],
        feature_snapshot={},
        risk_flags=[]
    )

def test_assign_risk_flags_empty_features(empty_signal):
    flags = assign_risk_flags(empty_signal)
    assert SignalRiskFlag.INSUFFICIENT_FEATURES in flags
    assert SignalRiskFlag.STRATEGY_ERROR in flags

def test_assign_risk_flags_data_quality(empty_signal):
    empty_signal.metadata = {"data_quality_warning": True}
    empty_signal.feature_snapshot = {"dummy": 1}
    empty_signal.reasons = ["Reason"]

    flags = assign_risk_flags(empty_signal)
    assert SignalRiskFlag.DATA_QUALITY_WARNING in flags
    assert SignalRiskFlag.INSUFFICIENT_FEATURES not in flags

def test_assign_risk_flags_low_liquidity(empty_signal):
    empty_signal.feature_snapshot = {"volume": 10000}
    empty_signal.reasons = ["Reason"]

    flags = assign_risk_flags(empty_signal)
    assert SignalRiskFlag.LOW_LIQUIDITY in flags

def test_merge_risk_flags():
    existing = [SignalRiskFlag.LOW_LIQUIDITY]
    new = [SignalRiskFlag.LOW_LIQUIDITY, SignalRiskFlag.HIGH_VOLATILITY]

    merged = merge_risk_flags(existing, new)
    assert len(merged) == 2
    assert SignalRiskFlag.LOW_LIQUIDITY in merged
    assert SignalRiskFlag.HIGH_VOLATILITY in merged

def test_risk_flags_to_text():
    flags = [SignalRiskFlag.LOW_LIQUIDITY, SignalRiskFlag.HIGH_VOLATILITY]
    text = risk_flags_to_text(flags)
    assert "LOW_LIQUIDITY" in text
    assert "HIGH_VOLATILITY" in text

    assert risk_flags_to_text([]) == "None"

def test_has_high_risk_flags():
    assert has_high_risk_flags([SignalRiskFlag.STRATEGY_ERROR]) is True
    assert has_high_risk_flags([SignalRiskFlag.INSUFFICIENT_FEATURES]) is True
    assert has_high_risk_flags([SignalRiskFlag.LOW_LIQUIDITY]) is False
