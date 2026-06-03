from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import DegradationDiagnosticKind, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    FoldPerformanceMetric,
    TemporalStabilityMetric,
    DegradationDiagnostic,
    create_degradation_diagnostic_id,
    _now_utc
)

def infer_degradation_severity(value: Optional[float]) -> str:
    if value is None:
        return "UNKNOWN"
    if value > 0:
        return "NONE" # Actually improved
    if value > -0.1:
        return "LOW"
    if value > -0.3:
        return "MEDIUM"
    return "HIGH"

def build_degradation_diagnostics(fold_metrics: List[FoldPerformanceMetric], temporal_metrics: List[TemporalStabilityMetric]) -> List[DegradationDiagnostic]:
    diagnostics = []

    degradations = [m.degradation_value for m in fold_metrics if isinstance(m.degradation_value, (int, float))]
    avg_deg = sum(degradations) / len(degradations) if degradations else None
    severity = infer_degradation_severity(avg_deg)

    diag = DegradationDiagnostic(
        diagnostic_id=create_degradation_diagnostic_id(),
        created_at_utc=_now_utc(),
        diagnostic_kind=DegradationDiagnosticKind.IS_TO_OOS_RETURN_DEGRADATION,
        value=avg_deg,
        severity_label=severity,
        diagnostic_notes=["Average degradation from In-Sample to Out-of-Sample."],
        diagnostic_valid=True,
        not_strategy_activation=True,
        not_investment_advice=True,
        research_data_only=True
    )

    errors = validate_degradation_diagnostics([diag])
    if errors:
        diag.diagnostic_valid = False
        diag.errors = errors
        diag.risk_flags.append(WalkForwardRiskFlag.DEGRADATION_DIAGNOSTIC_INVALID)

    diagnostics.append(diag)
    return diagnostics

def validate_degradation_diagnostics(items: List[DegradationDiagnostic]) -> List[str]:
    errors = []
    for d in items:
        if not d.not_strategy_activation:
            errors.append(f"Diagnostic {d.diagnostic_id} must be not_strategy_activation")
        if not d.not_investment_advice:
            errors.append(f"Diagnostic {d.diagnostic_id} must be not_investment_advice")
    return errors

def degradation_diagnostics_summary(items: List[DegradationDiagnostic]) -> Dict[str, Any]:
    valid_count = sum(1 for d in items if d.diagnostic_valid)
    return {
        "total_diagnostics": len(items),
        "valid_diagnostics": valid_count,
        "all_valid": valid_count == len(items) and len(items) > 0
    }

def degradation_diagnostics_to_text(items: List[DegradationDiagnostic], limit: int = 300) -> str:
    summary = degradation_diagnostics_summary(items)
    return f"Degradation Diagnostics: {summary['valid_diagnostics']}/{summary['total_diagnostics']} valid"
