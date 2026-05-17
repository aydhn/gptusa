
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticEvent, FailureModeAssessment, validate_failure_mode_assessment, create_diagnostic_event_id
from usa_signal_bot.core.enums import DiagnosticScope, FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality
import pytest

def test_diagnostic_event_id_generation():
    eid = create_diagnostic_event_id("AAPL")
    assert "AAPL" in eid
    assert eid.startswith("ev_")

def test_failure_mode_assessment_validation():
    assessment = FailureModeAssessment(
        assessment_id="test",
        created_at_utc="2023-01-01T00:00:00Z",
        failure_mode=FailureModeType.OVER_SIZING,
        severity=DiagnosticSeverity.HIGH,
        evidence_quality=DiagnosticEvidenceQuality.MODERATE,
        affected_scope=DiagnosticScope.TRADE,
        affected_name="test",
        event_count=-1, # Invalid
        loss_count=0
    )
    with pytest.raises(ValueError, match="Counts cannot be negative"):
        validate_failure_mode_assessment(assessment)
