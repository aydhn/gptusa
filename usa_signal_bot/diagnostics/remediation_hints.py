from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    FailureModeAssessment, StrategyDiagnosticResult, RemediationHint, create_remediation_hint_id
)
from usa_signal_bot.core.enums import RemediationHintType, DiagnosticSeverity, DiagnosticScope, DiagnosticEvidenceQuality
from datetime import datetime, timezone

def safe_action_for_hint_type(hint_type: RemediationHintType) -> str:
    actions = {
        RemediationHintType.REVIEW_RULES: "Investigate strategy rules for potential gaps in logic.",
        RemediationHintType.REVIEW_THRESHOLDS: "Consider evaluating indicator thresholds for better sensitivity.",
        RemediationHintType.REVIEW_REGIME_GATE: "Review regime gating parameters. A stricter local filter might be considered.",
        RemediationHintType.REVIEW_COST_FILTER: "Investigate transaction cost filters to avoid high-drag trades.",
        RemediationHintType.REVIEW_LIQUIDITY_FILTER: "Consider enforcing stricter liquidity minimums.",
        RemediationHintType.REVIEW_SIZING: "Review position sizing logic to ensure it respects risk budgets.",
        RemediationHintType.REVIEW_REBALANCE: "Evaluate rebalance frequency to reduce turnover drag.",
        RemediationHintType.REVIEW_SIGNAL_DECAY: "Investigate stale signals. Consider adding a time-to-live filter.",
        RemediationHintType.REVIEW_DATA_QUALITY: "Check data provider and symbol lifecycle data for anomalies.",
        RemediationHintType.INCREASE_SAMPLE_SIZE: "Increase sample size or backtest window to improve statistical confidence.",
        RemediationHintType.ADD_DIAGNOSTIC_TAGGING: "Add additional metadata tagging to signals to improve diagnostic resolution.",
        RemediationHintType.NO_ACTION_LOW_CONFIDENCE: "No action recommended due to noisy or insufficient evidence."
    }
    return actions.get(hint_type, "Review findings locally.")

def remediation_hint_for_failure_mode(assessment: FailureModeAssessment) -> RemediationHint:
    hint_type_mapping = {
        "LOW_SIGNAL_QUALITY": RemediationHintType.REVIEW_THRESHOLDS,
        "COST_DRAG_ERASED_EDGE": RemediationHintType.REVIEW_COST_FILTER,
        "HIGH_SLIPPAGE": RemediationHintType.REVIEW_COST_FILTER,
        "HIGH_MARKET_IMPACT": RemediationHintType.REVIEW_COST_FILTER,
        "HIGH_SPREAD": RemediationHintType.REVIEW_COST_FILTER,
        "LOW_LIQUIDITY": RemediationHintType.REVIEW_LIQUIDITY_FILTER,
        "REGIME_MISMATCH": RemediationHintType.REVIEW_REGIME_GATE,
        "TREND_REVERSAL": RemediationHintType.REVIEW_REGIME_GATE,
        "OVER_SIZING": RemediationHintType.REVIEW_SIZING,
        "UNDER_SIZING": RemediationHintType.REVIEW_SIZING,
        "RISK_BUDGET_EXHAUSTED": RemediationHintType.REVIEW_SIZING,
        "REBALANCE_TURNOVER_DRAG": RemediationHintType.REVIEW_REBALANCE,
        "SIGNAL_DECAY": RemediationHintType.REVIEW_SIGNAL_DECAY,
        "DATA_QUALITY_ISSUE": RemediationHintType.REVIEW_DATA_QUALITY,
        "CORPORATE_ACTION_RISK": RemediationHintType.REVIEW_DATA_QUALITY
    }

    hint_type = hint_type_mapping.get(assessment.failure_mode.value, RemediationHintType.REVIEW_RULES)

    if assessment.evidence_quality in [DiagnosticEvidenceQuality.NOISY, DiagnosticEvidenceQuality.INSUFFICIENT]:
        if assessment.event_count < 10: # Heuristic
            hint_type = RemediationHintType.INCREASE_SAMPLE_SIZE
        else:
            hint_type = RemediationHintType.NO_ACTION_LOW_CONFIDENCE

    return RemediationHint(
        hint_id=create_remediation_hint_id(hint_type),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        hint_type=hint_type,
        severity=assessment.severity,
        target_scope=assessment.affected_scope,
        target_name=assessment.affected_name,
        title=f"Review suggested for {assessment.failure_mode.value}",
        description=f"Evidence suggests {assessment.failure_mode.value} might be affecting performance. Please review locally.",
        evidence_refs=[assessment.assessment_id],
        safe_action=safe_action_for_hint_type(hint_type)
    )

def remediation_hints_from_assessments(assessments: List[FailureModeAssessment]) -> List[RemediationHint]:
    return [remediation_hint_for_failure_mode(a) for a in assessments]

def remediation_hints_from_strategy_diagnostics(results: List[StrategyDiagnosticResult]) -> List[RemediationHint]:
    hints = []
    for res in results:
        if res.status.value in ["DEGRADED", "FAILING"]:
            hints.append(RemediationHint(
                hint_id=create_remediation_hint_id(RemediationHintType.REVIEW_RULES),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                hint_type=RemediationHintType.REVIEW_RULES,
                severity=res.severity,
                target_scope=DiagnosticScope.STRATEGY,
                target_name=res.strategy_name,
                title=f"Review Strategy: {res.strategy_name}",
                description=f"Strategy {res.strategy_name} is in {res.status.value} status. Review rules locally.",
                evidence_refs=[res.diagnostic_id],
                safe_action=safe_action_for_hint_type(RemediationHintType.REVIEW_RULES)
            ))
    return hints

def remediation_hints_to_text(hints: List[RemediationHint], limit: int = 100) -> str:
    lines = [f"Remediation Hints (Total: {len(hints)}, Showing top {min(len(hints), limit)}):"]
    for h in hints[:limit]:
        lines.append(f"  [{h.target_name}] {h.title} -> {h.safe_action}")
    return "\n".join(lines)
