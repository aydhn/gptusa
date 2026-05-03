import pytest
import datetime
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket, SignalQualityStatus, SignalRejectionReason
from usa_signal_bot.core.config_schema import SignalQualityConfig
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.signal_quality import (
    evaluate_signal_quality,
    evaluate_signal_quality_list,
    reject_low_confidence,
    reject_low_score,
    reject_missing_reasons,
    reject_missing_feature_snapshot,
    reject_expired_signal,
    quality_report_to_text,
    assert_signal_quality_acceptable,
    SignalQualityGuardError
)

@pytest.fixture
def default_config():
    return SignalQualityConfig()

@pytest.fixture
def valid_signal():
    return StrategySignal(
        signal_id="TEST-123",
        strategy_name="TEST_STRAT",
        symbol="AAPL",
        timeframe="1d",
        timestamp_utc="2024-01-01T00:00:00Z",
        action=SignalAction.LONG,
        confidence=0.8,
        confidence_bucket=SignalConfidenceBucket.HIGH,
        score=60.0,
        reasons=["Good reason"],
        feature_snapshot={"price": 100},
        risk_flags=[]
    )

def test_reject_missing_reasons(valid_signal):
    assert reject_missing_reasons(valid_signal).passed is True
    valid_signal.reasons = []
    res = reject_missing_reasons(valid_signal)
    assert res.passed is False
    assert res.status == SignalQualityStatus.REJECTED
    assert res.rejection_reason == SignalRejectionReason.MISSING_REASONS

def test_reject_missing_feature_snapshot(valid_signal):
    assert reject_missing_feature_snapshot(valid_signal).passed is True
    valid_signal.feature_snapshot = {}
    res = reject_missing_feature_snapshot(valid_signal)
    assert res.passed is False
    assert res.status == SignalQualityStatus.REJECTED
    assert res.rejection_reason == SignalRejectionReason.MISSING_FEATURE_SNAPSHOT

def test_reject_expired_signal(valid_signal):
    now = datetime.datetime(2024, 1, 2, tzinfo=datetime.timezone.utc).isoformat()
    assert reject_expired_signal(valid_signal, now).passed is True

    valid_signal.expires_at_utc = datetime.datetime(2024, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc).isoformat()
    assert reject_expired_signal(valid_signal, now).passed is False

def test_reject_low_confidence(valid_signal, default_config):
    assert reject_low_confidence(valid_signal, 0.5).passed is True
    valid_signal.confidence = 0.1
    res = reject_low_confidence(valid_signal, 0.5)
    assert res.passed is False
    assert res.status == SignalQualityStatus.REJECTED
    assert res.rejection_reason == SignalRejectionReason.LOW_CONFIDENCE

def test_evaluate_signal_quality(valid_signal, default_config):
    results = evaluate_signal_quality(valid_signal, config=default_config)
    assert all(r.passed is True or r.status == SignalQualityStatus.WARNING for r in results)

def test_evaluate_signal_quality_list(valid_signal, default_config):
    report = evaluate_signal_quality_list([valid_signal], config=default_config)
    assert report.total_signals == 1
    assert report.accepted_count == 1
    assert report.rejected_count == 0

    valid_signal.reasons = []
    report2 = evaluate_signal_quality_list([valid_signal], config=default_config)
    assert report2.rejected_count == 1

def test_quality_report_to_text(valid_signal, default_config):
    report = evaluate_signal_quality_list([valid_signal], config=default_config)
    text = quality_report_to_text(report)
    assert "Accepted: 1" in text

def test_assert_signal_quality_acceptable(valid_signal, default_config):
    report = evaluate_signal_quality_list([valid_signal], config=default_config)
    assert_signal_quality_acceptable(report)

    report.errors.append("Fatal error")
    with pytest.raises(SignalQualityGuardError):
        assert_signal_quality_acceptable(report)
