from typing import Any, Dict, List

from usa_signal_bot.core.exceptions import RegimeDiagnosticsReadinessGateError
from usa_signal_bot.core.enums import (
    RegimeDiagnosticsReadinessStatus,
    RegimeDiagnosticsReadinessRuleKind,
    RegimeTransitionRiskFlag
)
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeLabelingIngestionResult,
    RegimeTransitionAnalyticsResult,
    RegimeDiagnosticsReadinessRule,
    RegimeDiagnosticsReadinessGate,
    create_regime_diagnostics_readiness_rule_id,
    create_regime_diagnostics_readiness_gate_id,
    _now
)

def _build_rule(kind: RegimeDiagnosticsReadinessRuleKind, name: str, passed: bool, required: bool, rationale: str) -> RegimeDiagnosticsReadinessRule:
    status = RegimeDiagnosticsReadinessStatus.PASSED if passed else (RegimeDiagnosticsReadinessStatus.FAILED if required else RegimeDiagnosticsReadinessStatus.WARNING)
    return RegimeDiagnosticsReadinessRule(
        rule_id=create_regime_diagnostics_readiness_rule_id(),
        created_at_utc=_now(),
        rule_kind=kind,
        name=name,
        status=status,
        required=required,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale=rationale
    )

def build_regime_diagnostics_readiness_rules(ingestion: RegimeLabelingIngestionResult, analytics: RegimeTransitionAnalyticsResult) -> List[RegimeDiagnosticsReadinessRule]:
    rules = []

    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.LABELING_VALID,
        "Phase 128 Ingestion Valid",
        ingestion.valid_for_phase129 and ingestion.ready_for_phase129,
        True,
        "Ingestion from Phase 128 must be valid and ready."
    ))

    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.LABEL_SEQUENCES_AVAILABLE,
        "Label Sequences Available",
        analytics.matrix_count > 0,
        True,
        "At least one transition matrix must be built."
    ))

    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.TRANSITION_MATRIX_VALID,
        "Transition Matrix Valid",
        all(m.matrix_valid for m in analytics.transition_matrices),
        True,
        "All built transition matrices must be valid."
    ))

    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.NO_SIGNAL_OUTPUT,
        "No Signal Output",
        not analytics.produces_trade_signal,
        True,
        "Must not produce trade signals."
    ))

    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.NO_ORDER_OUTPUT,
        "No Order Output",
        not analytics.produces_order_decision,
        True,
        "Must not produce order decisions."
    ))

    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.NO_PORTFOLIO_OUTPUT,
        "No Portfolio Output",
        not analytics.produces_portfolio_weights,
        True,
        "Must not produce portfolio weights."
    ))

    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.NO_EXECUTION_OUTPUT,
        "No Execution Output",
        not (analytics.activation_allowed or analytics.strategy_activation_allowed or analytics.deployment_allowed),
        True,
        "Must not allow activation or deployment."
    ))

    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.NO_MODEL_TRAINING,
        "No Model Training",
        not (analytics.model_training_used or analytics.model_prediction_used),
        True,
        "Must not use model training or prediction."
    ))

    passed_all = all(r.passed for r in rules if r.required)
    rules.append(_build_rule(
        RegimeDiagnosticsReadinessRuleKind.READY_FOR_PHASE130,
        "Ready for Phase 130",
        passed_all,
        True,
        "All required rules must pass to be ready for Phase 130."
    ))

    return rules

def build_regime_diagnostics_readiness_gate(ingestion: RegimeLabelingIngestionResult, analytics: RegimeTransitionAnalyticsResult) -> RegimeDiagnosticsReadinessGate:
    rules = build_regime_diagnostics_readiness_rules(ingestion, analytics)
    passed_all = all(r.passed for r in rules if r.required)
    status = RegimeDiagnosticsReadinessStatus.PASSED if passed_all else RegimeDiagnosticsReadinessStatus.FAILED

    risk_flags = []
    if not passed_all:
        risk_flags.append(RegimeTransitionRiskFlag.DIAGNOSTICS_READINESS_GATE_FAILED)

    return RegimeDiagnosticsReadinessGate(
        gate_id=create_regime_diagnostics_readiness_gate_id(),
        created_at_utc=_now(),
        status=status,
        rules=rules,
        analytics_result=analytics,
        ready_for_phase130=passed_all,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        risk_flags=risk_flags
    )

def regime_diagnostics_readiness_passed(gate: RegimeDiagnosticsReadinessGate) -> bool:
    return gate.status == RegimeDiagnosticsReadinessStatus.PASSED

def regime_diagnostics_readiness_blocks_phase130(gate: RegimeDiagnosticsReadinessGate) -> bool:
    return not gate.ready_for_phase130

def validate_regime_diagnostics_readiness_gate(gate: RegimeDiagnosticsReadinessGate) -> List[str]:
    errors = []
    if gate.status != RegimeDiagnosticsReadinessStatus.PASSED and gate.ready_for_phase130:
        errors.append("Gate marked ready for Phase 130 but status is not PASSED.")
    return errors

def regime_diagnostics_readiness_gate_summary(gate: RegimeDiagnosticsReadinessGate) -> Dict[str, Any]:
    return {
        "status": gate.status.value,
        "ready_for_phase130": gate.ready_for_phase130,
        "rules_total": len(gate.rules),
        "rules_passed": sum(1 for r in gate.rules if r.passed)
    }

def regime_diagnostics_readiness_gate_to_text(gate: RegimeDiagnosticsReadinessGate, limit: int = 300) -> str:
    lines = [
        f"Regime Diagnostics Readiness Gate: {gate.status.value}",
        f"Ready for Phase 130: {gate.ready_for_phase130}"
    ]
    for r in gate.rules:
        lines.append(f" - {r.name}: {'PASS' if r.passed else 'FAIL'}")
    return "\n".join(lines)
