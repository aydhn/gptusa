from typing import Any
from datetime import datetime, timezone
from .diagnostic_models import DiagnosticEvent, FailureModeAssessment, FailureCluster, create_failure_mode_assessment_id, create_failure_cluster_id
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope, FailureClusterType

def filter_losing_events(events: list[DiagnosticEvent]) -> list[DiagnosticEvent]:
    return [e for e in events if e.net_pnl_usd is not None and e.net_pnl_usd < 0]

def loss_summary(events: list[DiagnosticEvent]) -> dict[str, Any]:
    losers = filter_losing_events(events)
    total_loss = sum((e.net_pnl_usd for e in losers if e.net_pnl_usd), 0.0)
    return {
        "total_events": len(events),
        "loss_count": len(losers),
        "total_net_loss_usd": total_loss,
        "loss_rate": len(losers) / len(events) if events else 0.0
    }
