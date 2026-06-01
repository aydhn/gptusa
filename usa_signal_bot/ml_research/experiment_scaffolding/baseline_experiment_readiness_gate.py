from typing import List, Dict, Any
from usa_signal_bot.core.enums import BaselineScaffoldingReadinessRuleKind, BaselineScaffoldingReadinessStatus
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineExperimentReadinessGate,
    BaselineExperimentReadinessRule,
    BaselineExperimentRegistry,
    EvaluationHarnessContract,
    PredictionOutputBoundary,
    NonActivationEvaluationBoundaryResult,
    MLDatasetAssemblyIngestionResult,
    create_baseline_experiment_readiness_rule_id,
    create_baseline_experiment_readiness_gate_id,
    _now_utc
)

def build_baseline_experiment_readiness_rules(ingestion: MLDatasetAssemblyIngestionResult, registry: BaselineExperimentRegistry, harness: EvaluationHarnessContract, boundary: PredictionOutputBoundary, non_activation: NonActivationEvaluationBoundaryResult) -> List[BaselineExperimentReadinessRule]:
    rules = []

    def add_rule(kind: BaselineScaffoldingReadinessRuleKind, name: str, passed: bool, rationale: str):
        status = BaselineScaffoldingReadinessStatus.PASSED if passed else BaselineScaffoldingReadinessStatus.FAILED
        rules.append(BaselineExperimentReadinessRule(
            rule_id=create_baseline_experiment_readiness_rule_id(),
            created_at_utc=_now_utc(),
            rule_kind=kind,
            name=name,
            status=status,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale=rationale
        ))

    add_rule(BaselineScaffoldingReadinessRuleKind.DATASET_ASSEMBLY_VALID, "Dataset Assembly Valid", ingestion.ready_for_phase138, "Phase 137 assembly must be ready")
    add_rule(BaselineScaffoldingReadinessRuleKind.EXPERIMENT_SPECS_VALID, "Experiment Specs Valid", len(registry.experiment_specs) > 0, "Must have experiment specs")
    add_rule(BaselineScaffoldingReadinessRuleKind.EVALUATION_HARNESS_CONTRACT_VALID, "Harness Valid", harness.contract_valid, "Harness contract must be valid")
    add_rule(BaselineScaffoldingReadinessRuleKind.PREDICTION_OUTPUT_BOUNDARY_VALID, "Prediction Boundary Valid", boundary.boundary_valid, "Prediction boundary must be valid")
    add_rule(BaselineScaffoldingReadinessRuleKind.NON_ACTIVATION_BOUNDARY_VALID, "Non-Activation Valid", non_activation.boundary_passed, "Non-activation boundary must pass")
    add_rule(BaselineScaffoldingReadinessRuleKind.EXPERIMENT_REGISTRY_VALID, "Registry Valid", registry.registry_valid, "Experiment registry must be valid")
    add_rule(BaselineScaffoldingReadinessRuleKind.NO_MODEL_TRAINING, "No Model Training", not registry.training_started, "Must not have started training")
    add_rule(BaselineScaffoldingReadinessRuleKind.NO_MODEL_PREDICTION, "No Model Prediction", not registry.prediction_started, "Must not have started prediction")

    return rules

def build_baseline_experiment_readiness_gate(ingestion: MLDatasetAssemblyIngestionResult, registry: BaselineExperimentRegistry, harness: EvaluationHarnessContract, boundary: PredictionOutputBoundary, non_activation: NonActivationEvaluationBoundaryResult) -> BaselineExperimentReadinessGate:
    rules = build_baseline_experiment_readiness_rules(ingestion, registry, harness, boundary, non_activation)
    passed = all(r.passed for r in rules if r.required)

    return BaselineExperimentReadinessGate(
        gate_id=create_baseline_experiment_readiness_gate_id(),
        created_at_utc=_now_utc(),
        status=BaselineScaffoldingReadinessStatus.PASSED if passed else BaselineScaffoldingReadinessStatus.BLOCKED,
        rules=rules,
        experiment_registry=registry,
        evaluation_harness_contract=harness,
        prediction_output_boundary=boundary,
        non_activation_boundary=non_activation,
        ready_for_phase139=passed,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        training_started=False,
        prediction_started=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

def baseline_experiment_readiness_passed(gate: BaselineExperimentReadinessGate) -> bool:
    return gate.ready_for_phase139

def baseline_experiment_readiness_blocks_phase139(gate: BaselineExperimentReadinessGate) -> bool:
    return not gate.ready_for_phase139

def validate_baseline_experiment_readiness_gate(gate: BaselineExperimentReadinessGate) -> List[str]:
    errors = []
    if gate.ready_for_phase139 and gate.status != BaselineScaffoldingReadinessStatus.PASSED:
        errors.append("Gate is ready but status is not PASSED")
    return errors

def baseline_experiment_readiness_gate_summary(gate: BaselineExperimentReadinessGate) -> Dict[str, Any]:
    return {
        "passed": gate.ready_for_phase139,
        "status": gate.status.value,
        "rules_total": len(gate.rules),
        "rules_passed": sum(1 for r in gate.rules if r.passed)
    }

def baseline_experiment_readiness_gate_to_text(gate: BaselineExperimentReadinessGate, limit: int = 300) -> str:
    summary = baseline_experiment_readiness_gate_summary(gate)
    return f"Readiness Gate: Passed={summary['passed']} ({summary['rules_passed']}/{summary['rules_total']} rules)"
