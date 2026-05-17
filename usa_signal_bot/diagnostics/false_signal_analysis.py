from typing import Any
from datetime import datetime, timezone
from .diagnostic_models import DiagnosticEvent, FailureModeAssessment, create_failure_mode_assessment_id
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope

def identify_false_positive_events(events: list[DiagnosticEvent], min_signal_score: float = 70.0, negative_pnl_required: bool = True) -> list[DiagnosticEvent]:
    false_positives = []
    for e in events:
        if e.signal_score is not None and e.signal_score >= min_signal_score:
            if negative_pnl_required:
                if e.net_pnl_usd is not None and e.net_pnl_usd < 0:
                    false_positives.append(e)
            else:
                false_positives.append(e)
    return false_positives
