import hashlib
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import WalkForwardQuality, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    OOSRobustnessMetrics,
    TemporalStabilityMetric,
    DegradationDiagnostic,
    RobustnessSummary,
    create_robustness_summary_id,
    _now_utc
)

def infer_walk_forward_quality(summary: RobustnessSummary) -> WalkForwardQuality:
    if not summary.summary_valid:
        return WalkForwardQuality.INVALID

    score = summary.oos_metrics.robustness_score
    if score is None:
        return WalkForwardQuality.UNKNOWN

    if score > 80:
        return WalkForwardQuality.HIGH
    if score > 50:
        return WalkForwardQuality.ACCEPTABLE
    if score > 20:
        return WalkForwardQuality.WARNING
    return WalkForwardQuality.LOW

def compute_robustness_summary_hash(summary: RobustnessSummary) -> str:
    content = f"{summary.fold_count}:{summary.oos_metrics.robustness_score}:{summary.not_investment_advice}:{summary.not_strategy_activation}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def build_robustness_summary(
    oos_metrics: OOSRobustnessMetrics,
    temporal_metrics: List[TemporalStabilityMetric],
    degradation_diagnostics: List[DegradationDiagnostic]
) -> RobustnessSummary:
    summary = RobustnessSummary(
        summary_id=create_robustness_summary_id(),
        created_at_utc=_now_utc(),
        fold_count=oos_metrics.fold_count,
        oos_metrics=oos_metrics,
        temporal_stability_metrics=temporal_metrics,
        degradation_diagnostics=degradation_diagnostics,
        summary_hash=None,
        summary_valid=True,
        robustness_quality=WalkForwardQuality.UNKNOWN,
        not_investment_advice=True,
        not_strategy_activation=True,
        research_data_only=True
    )

    errors = validate_robustness_summary(summary)
    if errors:
        summary.summary_valid = False
        summary.errors = errors
        summary.risk_flags.append(WalkForwardRiskFlag.ROBUSTNESS_SUMMARY_INVALID)

    summary.robustness_quality = infer_walk_forward_quality(summary)
    summary.summary_hash = compute_robustness_summary_hash(summary)

    return summary

def validate_robustness_summary(summary: RobustnessSummary) -> List[str]:
    errors = []
    if not summary.not_investment_advice:
        errors.append("Summary must be not_investment_advice")
    if not summary.not_strategy_activation:
        errors.append("Summary must be not_strategy_activation")
    if not summary.oos_metrics.metrics_valid:
        errors.append("OOS metrics invalid inside summary")
    return errors

def robustness_summary_to_text(summary: RobustnessSummary, limit: int = 300) -> str:
    lines = [
        f"Robustness Summary:",
        f"  Valid: {summary.summary_valid}",
        f"  Quality: {summary.robustness_quality.value}",
        f"  Score: {summary.oos_metrics.robustness_score}"
    ]
    return "\n".join(lines)[:limit]
