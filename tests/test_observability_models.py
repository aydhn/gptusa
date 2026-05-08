from usa_signal_bot.observability.observability_models import ObservabilityEvent, OperationalMetric, LogFileSummary, LogRotationResult, OperationalMetricsSnapshot, OperationalHealthReport, create_observability_event_id, validate_observability_event
from usa_signal_bot.core.enums import ObservabilityEventType, ObservabilitySeverity, MetricType, OperationalMetricStatus, LogRotationStatus, OperationalHealthStatus, DiskUsageStatus, SafetyMonitorStatus
import pytest

def test_observability_event_creation():
    e = ObservabilityEvent(
        event_id=create_observability_event_id(),
        event_type=ObservabilityEventType.CUSTOM,
        severity=ObservabilitySeverity.INFO,
        timestamp_utc="2026-05-08T00:00:00Z",
        source="test",
        message="Hello world"
    )
    assert e.source == "test"
    validate_observability_event(e)

def test_validation_fails_on_empty():
    e = ObservabilityEvent("1", ObservabilityEventType.CUSTOM, ObservabilitySeverity.INFO, "now", "", "msg")
    with pytest.raises(ValueError):
        validate_observability_event(e)

def test_validation_fails_on_token_leak():
    e = ObservabilityEvent("1", ObservabilityEventType.CUSTOM, ObservabilitySeverity.INFO, "now", "src", "msg", payload={"token": "123"})
    with pytest.raises(ValueError):
        validate_observability_event(e)
