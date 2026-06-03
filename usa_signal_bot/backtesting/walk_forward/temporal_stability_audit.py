import hashlib
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    RobustnessSummary,
    TemporalStabilityMetric,
    DegradationDiagnostic,
    TemporalStabilityAuditReport,
    create_temporal_stability_audit_id,
    _now_utc
)

def compute_temporal_stability_audit_hash(audit: TemporalStabilityAuditReport) -> str:
    content = f"{audit.audit_id}:{audit.robustness_summary.summary_hash}:{audit.no_strategy_activation}:{audit.no_investment_advice}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def build_temporal_stability_audit(summary: RobustnessSummary) -> TemporalStabilityAuditReport:
    audit = TemporalStabilityAuditReport(
        audit_id=create_temporal_stability_audit_id(),
        created_at_utc=_now_utc(),
        robustness_summary=summary,
        stability_metrics=summary.temporal_stability_metrics,
        degradation_diagnostics=summary.degradation_diagnostics,
        audit_passed=True,
        audit_quality=summary.robustness_quality,
        audit_hash=None,
        no_strategy_activation=True,
        no_investment_advice=True,
        research_data_only=True
    )

    errors = validate_temporal_stability_audit(audit)
    if errors:
        audit.audit_passed = False
        audit.errors = errors
        audit.risk_flags.append(WalkForwardRiskFlag.TEMPORAL_STABILITY_AUDIT_INVALID)

    audit.audit_hash = compute_temporal_stability_audit_hash(audit)
    return audit

def validate_temporal_stability_audit(audit: TemporalStabilityAuditReport) -> List[str]:
    errors = []
    if not audit.no_strategy_activation:
        errors.append("no_strategy_activation must be true")
    if not audit.no_investment_advice:
        errors.append("no_investment_advice must be true")
    if not audit.robustness_summary.summary_valid:
        errors.append("robustness_summary is invalid")
    return errors

def temporal_stability_audit_summary(audit: TemporalStabilityAuditReport) -> Dict[str, Any]:
    return {
        "passed": audit.audit_passed,
        "quality": audit.audit_quality.value
    }

def temporal_stability_audit_to_text(audit: TemporalStabilityAuditReport, limit: int = 300) -> str:
    summary = temporal_stability_audit_summary(audit)
    lines = [
        f"Temporal Stability Audit:",
        f"  Passed: {summary['passed']}",
        f"  Quality: {summary['quality']}"
    ]
    return "\n".join(lines)[:limit]
