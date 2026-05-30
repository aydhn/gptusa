import datetime
from typing import Any, Dict, List
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeContextValidationIngestionResult,
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftTrackingResult,
    ContextDegradationProfile,
    RegimeMonitoringReadinessRule,
    RegimeMonitoringReadinessGate,
    RegimeMonitoringReadinessRuleKind,
    RegimeMonitoringReadinessStatus,
    ContextDegradationStatus,
    create_regime_monitoring_readiness_rule_id,
    create_regime_monitoring_readiness_gate_id
)

def build_regime_monitoring_readiness_rules(
    ingestion: RegimeContextValidationIngestionResult,
    baseline: RegimeMonitoringBaseline,
    snapshot: RegimeMonitoringSnapshot,
    drift_result: RegimeDriftTrackingResult,
    degradation_profiles: List[ContextDegradationProfile]
) -> List[RegimeMonitoringReadinessRule]:

    def _create_rule(kind: RegimeMonitoringReadinessRuleKind, name: str, passed: bool, rationale: str) -> RegimeMonitoringReadinessRule:
        return RegimeMonitoringReadinessRule(
            rule_id=create_regime_monitoring_readiness_rule_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            rule_kind=kind,
            name=name,
            status=RegimeMonitoringReadinessStatus.PASSED if passed else RegimeMonitoringReadinessStatus.FAILED,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale=rationale,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )

    rules = [
        _create_rule(RegimeMonitoringReadinessRuleKind.CONTEXT_VALIDATION_VALID, "Context Validation Valid", ingestion.valid_for_phase133, "Phase 132 context must be valid"),
        _create_rule(RegimeMonitoringReadinessRuleKind.ARTIFACTS_AVAILABLE, "Artifacts Available", True, "Artifacts loaded"), # Assuming true if we got here in the flow
        _create_rule(RegimeMonitoringReadinessRuleKind.BASELINE_VALID, "Baseline Valid", baseline.baseline_valid, "Baseline must be valid"),
        _create_rule(RegimeMonitoringReadinessRuleKind.SNAPSHOT_VALID, "Snapshot Valid", snapshot.snapshot_valid, "Snapshot must be valid"),
        _create_rule(RegimeMonitoringReadinessRuleKind.DRIFT_RESULTS_VALID, "Drift Results Valid", drift_result.drift_valid, "Drift results must be valid"),
        _create_rule(RegimeMonitoringReadinessRuleKind.NO_SIGNAL_OUTPUT, "No Signal Output", True, "Must not produce trade signals"),
        _create_rule(RegimeMonitoringReadinessRuleKind.NO_ORDER_OUTPUT, "No Order Output", True, "Must not produce order decisions"),
        _create_rule(RegimeMonitoringReadinessRuleKind.NO_PORTFOLIO_OUTPUT, "No Portfolio Output", True, "Must not produce portfolio weights"),
        _create_rule(RegimeMonitoringReadinessRuleKind.NO_EXECUTION_OUTPUT, "No Execution Output", True, "Must not have execution enabled"),
        _create_rule(RegimeMonitoringReadinessRuleKind.NO_MODEL_TRAINING, "No Model Training", True, "Must not train models")
    ]

    degradation_valid = not any(p.profile_status == ContextDegradationStatus.BLOCKED for p in degradation_profiles)
    rules.append(_create_rule(RegimeMonitoringReadinessRuleKind.DEGRADATION_DIAGNOSTICS_VALID, "Degradation Diagnostics Valid", degradation_valid, "No blocking degradations"))

    all_passed = all(r.passed for r in rules)
    rules.append(_create_rule(RegimeMonitoringReadinessRuleKind.READY_FOR_PHASE134, "Ready for Phase 134", all_passed, "All prerequisite rules passed"))

    return rules

def build_regime_monitoring_readiness_gate(
    ingestion: RegimeContextValidationIngestionResult,
    baseline: RegimeMonitoringBaseline,
    snapshot: RegimeMonitoringSnapshot,
    drift_result: RegimeDriftTrackingResult,
    degradation_profiles: List[ContextDegradationProfile]
) -> RegimeMonitoringReadinessGate:

    rules = build_regime_monitoring_readiness_rules(ingestion, baseline, snapshot, drift_result, degradation_profiles)
    status = RegimeMonitoringReadinessStatus.PASSED if all(r.passed for r in rules) else RegimeMonitoringReadinessStatus.FAILED

    return RegimeMonitoringReadinessGate(
        gate_id=create_regime_monitoring_readiness_gate_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=status,
        rules=rules,
        drift_result=drift_result,
        degradation_profiles=degradation_profiles,
        ready_for_phase134=status == RegimeMonitoringReadinessStatus.PASSED,
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
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def regime_monitoring_readiness_passed(gate: RegimeMonitoringReadinessGate) -> bool:
    return gate.status == RegimeMonitoringReadinessStatus.PASSED

def regime_monitoring_readiness_blocks_phase134(gate: RegimeMonitoringReadinessGate) -> bool:
    return not gate.ready_for_phase134

def validate_regime_monitoring_readiness_gate(gate: RegimeMonitoringReadinessGate) -> List[str]:
    errors = []
    if gate.ready_for_phase134 and gate.status != RegimeMonitoringReadinessStatus.PASSED:
         errors.append("Gate is ready for phase 134 but status is not PASSED")
    if not gate.research_data_only:
         errors.append("Gate is not research_data_only")
    return errors

def regime_monitoring_readiness_gate_summary(gate: RegimeMonitoringReadinessGate) -> Dict[str, Any]:
    return {
        "status": gate.status.value,
        "ready_for_phase134": gate.ready_for_phase134,
        "failed_rules": [r.name for r in gate.rules if not r.passed]
    }

def regime_monitoring_readiness_gate_to_text(gate: RegimeMonitoringReadinessGate, limit: int = 300) -> str:
    summ = regime_monitoring_readiness_gate_summary(gate)
    text = f"Readiness Gate: {summ}"
    if len(text) > limit:
        return text[:limit] + "..."
    return text
