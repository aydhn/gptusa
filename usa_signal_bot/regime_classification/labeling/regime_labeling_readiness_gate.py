from typing import Any
from usa_signal_bot.core.enums import (
    RegimeLabelingReadinessRuleKind,
    RegimeLabelingReadinessStatus,
    RegimeLabelingRiskFlag
)
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeFeatureEngineeringIngestionResult,
    HeuristicRegimeLabelResult,
    RollingRegimeWindowResult,
    RegimeCandidateValidationResult,
    RegimeLabelStabilityProfile,
    RegimeLabelingReadinessRule,
    RegimeLabelingReadinessGate,
    create_regime_labeling_readiness_rule_id,
    create_regime_labeling_readiness_gate_id,
    _now_utc
)

def build_regime_labeling_readiness_rules(
    ingestion: RegimeFeatureEngineeringIngestionResult,
    label_results: list[HeuristicRegimeLabelResult],
    window_results: list[RollingRegimeWindowResult],
    candidate_validation: RegimeCandidateValidationResult,
    stability_profiles: list[RegimeLabelStabilityProfile]
) -> list[RegimeLabelingReadinessRule]:

    rules = []

    # 1. FEATURE_ENGINEERING_VALID
    passed_fe = ingestion.valid_for_phase128 and ingestion.ready_for_phase128
    rules.append(RegimeLabelingReadinessRule(
        rule_id=create_regime_labeling_readiness_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeLabelingReadinessRuleKind.FEATURE_ENGINEERING_VALID,
        name="Feature Engineering Ingestion Valid",
        status=RegimeLabelingReadinessStatus.PASSED if passed_fe else RegimeLabelingReadinessStatus.FAILED,
        required=True,
        passed=passed_fe,
        expected_value=True,
        observed_value=passed_fe,
        rationale="Must have valid Phase 127 ingestion"
    ))

    # 2. HEURISTIC_LABELS_VALID
    passed_hl = len(label_results) > 0
    rules.append(RegimeLabelingReadinessRule(
        rule_id=create_regime_labeling_readiness_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeLabelingReadinessRuleKind.HEURISTIC_LABELS_VALID,
        name="Heuristic Labels Valid",
        status=RegimeLabelingReadinessStatus.PASSED if passed_hl else RegimeLabelingReadinessStatus.FAILED,
        required=True,
        passed=passed_hl,
        expected_value="> 0 results",
        observed_value=len(label_results),
        rationale="Must have generated labels"
    ))

    # 3. ROLLING_WINDOWS_VALID
    passed_rw = len(window_results) > 0
    rules.append(RegimeLabelingReadinessRule(
        rule_id=create_regime_labeling_readiness_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeLabelingReadinessRuleKind.ROLLING_WINDOWS_VALID,
        name="Rolling Windows Valid",
        status=RegimeLabelingReadinessStatus.PASSED if passed_rw else RegimeLabelingReadinessStatus.FAILED,
        required=True,
        passed=passed_rw,
        expected_value="> 0 results",
        observed_value=len(window_results),
        rationale="Must have generated windows"
    ))

    # 4. CANDIDATE_VALIDATION_PASSED
    passed_cv = candidate_validation.validation_passed if candidate_validation else False
    rules.append(RegimeLabelingReadinessRule(
        rule_id=create_regime_labeling_readiness_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeLabelingReadinessRuleKind.CANDIDATE_VALIDATION_PASSED,
        name="Candidate Validation Passed",
        status=RegimeLabelingReadinessStatus.PASSED if passed_cv else RegimeLabelingReadinessStatus.FAILED,
        required=True,
        passed=passed_cv,
        expected_value=True,
        observed_value=passed_cv,
        rationale="Candidate validation must pass"
    ))

    # 5. NO_EXECUTION_OUTPUT
    passed_exec = not any([
        ingestion.produces_trade_signal,
        ingestion.produces_order_decision,
        ingestion.produces_portfolio_weights,
        ingestion.investment_advice,
        candidate_validation.produces_trade_signal if candidate_validation else False
    ])
    rules.append(RegimeLabelingReadinessRule(
        rule_id=create_regime_labeling_readiness_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeLabelingReadinessRuleKind.NO_EXECUTION_OUTPUT,
        name="No Execution Output",
        status=RegimeLabelingReadinessStatus.PASSED if passed_exec else RegimeLabelingReadinessStatus.FAILED,
        required=True,
        passed=passed_exec,
        expected_value=False,
        observed_value=not passed_exec,
        rationale="Regime labeling must not produce execution signals"
    ))

    # 6. NO_MODEL_TRAINING
    passed_mt = not any([
        ingestion.model_training_used,
        ingestion.heavy_ml_dependency_used,
        not candidate_validation.no_model_training if candidate_validation else False
    ])
    rules.append(RegimeLabelingReadinessRule(
        rule_id=create_regime_labeling_readiness_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeLabelingReadinessRuleKind.NO_MODEL_TRAINING,
        name="No Model Training",
        status=RegimeLabelingReadinessStatus.PASSED if passed_mt else RegimeLabelingReadinessStatus.FAILED,
        required=True,
        passed=passed_mt,
        expected_value=False,
        observed_value=not passed_mt,
        rationale="Phase 128 is deterministic/heuristic, no model training"
    ))

    return rules

def build_regime_labeling_readiness_gate(
    ingestion: RegimeFeatureEngineeringIngestionResult,
    label_results: list[HeuristicRegimeLabelResult],
    window_results: list[RollingRegimeWindowResult],
    candidate_validation: RegimeCandidateValidationResult,
    stability_profiles: list[RegimeLabelStabilityProfile]
) -> RegimeLabelingReadinessGate:

    rules = build_regime_labeling_readiness_rules(ingestion, label_results, window_results, candidate_validation, stability_profiles)

    passed = all(r.passed for r in rules if r.required)

    flags = []
    if not passed:
        flags.append(RegimeLabelingRiskFlag.CANDIDATE_READINESS_GATE_FAILED)

    return RegimeLabelingReadinessGate(
        gate_id=create_regime_labeling_readiness_gate_id(),
        created_at_utc=_now_utc(),
        status=RegimeLabelingReadinessStatus.PASSED if passed else RegimeLabelingReadinessStatus.FAILED,
        rules=rules,
        candidate_validation=candidate_validation,
        stability_profiles=stability_profiles,
        ready_for_phase129=passed,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=not all(r.passed for r in rules if r.rule_kind == RegimeLabelingReadinessRuleKind.NO_MODEL_TRAINING),
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        risk_flags=flags
    )

def regime_labeling_readiness_passed(gate: RegimeLabelingReadinessGate) -> bool:
    return gate.status == RegimeLabelingReadinessStatus.PASSED

def regime_labeling_readiness_blocks_phase129(gate: RegimeLabelingReadinessGate) -> bool:
    return not gate.ready_for_phase129

def validate_regime_labeling_readiness_gate(gate: RegimeLabelingReadinessGate) -> list[str]:
    errors = []
    if gate.produces_trade_signal or gate.produces_order_decision or gate.produces_portfolio_weights:
        errors.append("Gate produces execution outputs")
    if gate.model_training_used or gate.model_prediction_used:
        errors.append("Gate allowed model training or prediction")
    return errors

def regime_labeling_readiness_gate_summary(gate: RegimeLabelingReadinessGate) -> dict[str, Any]:
    return {
        "status": gate.status.value,
        "ready_for_phase129": gate.ready_for_phase129,
        "rules_passed": sum(1 for r in gate.rules if r.passed)
    }

def regime_labeling_readiness_gate_to_text(gate: RegimeLabelingReadinessGate, limit: int = 300) -> str:
    return f"Readiness Gate: {gate.status.value}, Ready for 129: {gate.ready_for_phase129}"
