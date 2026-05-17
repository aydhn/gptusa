import pytest
import datetime
from datetime import timezone
from usa_signal_bot.portfolio_rebalance.signal_decay import (
    estimate_signal_age_minutes, signal_decay_multiplier, classify_signal_decay_severity,
    signal_valid_for_rebalance, signal_decay_drift_measurement
)
from usa_signal_bot.core.enums import DriftSeverity

def test_estimate_signal_age_minutes():
    now = datetime.datetime.now(timezone.utc)
    past = now - datetime.timedelta(minutes=120)
    signal = {"timestamp_utc": past.isoformat()}
    age = estimate_signal_age_minutes(signal, now_utc=now.isoformat())
    assert 119 < age < 121

def test_signal_decay_multiplier():
    assert signal_decay_multiplier(120.0, half_life_minutes=240.0) == 0.5
    assert signal_decay_multiplier(240.0, half_life_minutes=240.0) == 0.0
    assert signal_decay_multiplier(300.0, half_life_minutes=240.0) == 0.0

def test_classify_signal_decay_severity():
    assert classify_signal_decay_severity(120, max_age_minutes=1440) == DriftSeverity.NONE
    assert classify_signal_decay_severity(400, max_age_minutes=1440) == DriftSeverity.LOW
    assert classify_signal_decay_severity(800, max_age_minutes=1440) == DriftSeverity.MODERATE
    assert classify_signal_decay_severity(1200, max_age_minutes=1440) == DriftSeverity.HIGH
    assert classify_signal_decay_severity(1500, max_age_minutes=1440) == DriftSeverity.CRITICAL

def test_signal_valid_for_rebalance():
    now = datetime.datetime.now(timezone.utc)
    signal1 = {"timestamp_utc": (now - datetime.timedelta(minutes=1000)).isoformat()}
    signal2 = {"timestamp_utc": (now - datetime.timedelta(minutes=2000)).isoformat()}
    assert signal_valid_for_rebalance(signal1, max_age_minutes=1440) is True
    assert signal_valid_for_rebalance(signal2, max_age_minutes=1440) is False

def test_signal_decay_drift_measurement():
    now = datetime.datetime.now(timezone.utc)
    signal = {"timestamp_utc": (now - datetime.timedelta(minutes=120)).isoformat()}
    drift = signal_decay_drift_measurement("AAPL", signal)
    assert drift.name == "SignalDecay_AAPL"
    assert abs(drift.target_value - 0.5) < 0.01 # with default half-life 240
    assert drift.severity == DriftSeverity.NONE
