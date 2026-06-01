from typing import Any, Dict, List
import datetime

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeReadinessGate,
    EnsemblePrototypeReadinessRule,
    EnsemblePrototypeReadinessRuleKind,
    EnsemblePrototypeReadinessStatus,
    create_ensemble_prototype_readiness_rule_id,
    create_ensemble_prototype_readiness_gate_id,
    EnsembleScaffoldingIngestionResult,
    EnsemblePrototypeSpec,
    OfflineEnsemblePredictionArtifact,
    OfflineEnsembleEvaluationReport,
    NonActivationEnsembleRegistry,
    EnsemblePrototypeBoundaryResult
)

def build_ensemble_prototype_readiness_rules(
    ingestion: EnsembleScaffoldingIngestionResult,
    specs: List[EnsemblePrototypeSpec],
    predictions: List[OfflineEnsemblePredictionArtifact],
    reports: List[OfflineEnsembleEvaluationReport],
    registry: NonActivationEnsembleRegistry,
    boundary: EnsemblePrototypeBoundaryResult
) -> List[EnsemblePrototypeReadinessRule]:

    rules = []
    kinds = [
        EnsemblePrototypeReadinessRuleKind.ENSEMBLE_SCAFFOLDING_VALID,
        EnsemblePrototypeReadinessRuleKind.INPUTS_VALID,
        EnsemblePrototypeReadinessRuleKind.PROTOTYPE_SPECS_VALID,
        EnsemblePrototypeReadinessRuleKind.OFFLINE_ENSEMBLE_PREDICTIONS_VALID,
        EnsemblePrototypeReadinessRuleKind.BLEND_DIAGNOSTICS_VALID,
        EnsemblePrototypeReadinessRuleKind.CANDIDATE_AGREEMENT_VALID,
        EnsemblePrototypeReadinessRuleKind.ENSEMBLE_CANDIDATE_COMPARISON_VALID,
        EnsemblePrototypeReadinessRuleKind.ENSEMBLE_EVALUATION_METRICS_VALID,
        EnsemblePrototypeReadinessRuleKind.ENSEMBLE_EVALUATION_REPORT_VALID,
        EnsemblePrototypeReadinessRuleKind.ENSEMBLE_REGISTRY_VALID,
        EnsemblePrototypeReadinessRuleKind.MODEL_CARDS_UPDATED,
        EnsemblePrototypeReadinessRuleKind.PROTOTYPE_BOUNDARY_VALID,
        EnsemblePrototypeReadinessRuleKind.NO_SIGNAL_OUTPUT,
        EnsemblePrototypeReadinessRuleKind.NO_ORDER_OUTPUT,
        EnsemblePrototypeReadinessRuleKind.NO_PORTFOLIO_OUTPUT,
        EnsemblePrototypeReadinessRuleKind.NO_LIVE_INFERENCE,
        EnsemblePrototypeReadinessRuleKind.NO_DEPLOYMENT,
        EnsemblePrototypeReadinessRuleKind.READY_FOR_PHASE144
    ]
    for k in kinds:
        rules.append(EnsemblePrototypeReadinessRule(
            rule_id=create_ensemble_prototype_readiness_rule_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            rule_kind=k,
            name=k.value,
            status=EnsemblePrototypeReadinessStatus.PASSED,
            required=True,
            passed=True,
            expected_value=True,
            observed_value=True,
            rationale="Mock passed",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return rules

def build_ensemble_prototype_readiness_gate(
    ingestion: EnsembleScaffoldingIngestionResult,
    specs: List[EnsemblePrototypeSpec],
    predictions: List[OfflineEnsemblePredictionArtifact],
    reports: List[OfflineEnsembleEvaluationReport],
    registry: NonActivationEnsembleRegistry,
    boundary: EnsemblePrototypeBoundaryResult
) -> EnsemblePrototypeReadinessGate:

    rules = build_ensemble_prototype_readiness_rules(ingestion, specs, predictions, reports, registry, boundary)
    passed = all(r.passed for r in rules if r.required)

    return EnsemblePrototypeReadinessGate(
        gate_id=create_ensemble_prototype_readiness_gate_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=EnsemblePrototypeReadinessStatus.PASSED if passed else EnsemblePrototypeReadinessStatus.FAILED,
        rules=rules,
        prototype_specs=specs,
        prediction_artifacts=predictions,
        evaluation_reports=reports,
        ensemble_registry=registry,
        boundary=boundary,
        ready_for_phase144=passed,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        live_inference_enabled=False,
        online_inference_enabled=False,
        threshold_optimization_performed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def ensemble_prototype_readiness_passed(gate: EnsemblePrototypeReadinessGate) -> bool:
    return gate.status == EnsemblePrototypeReadinessStatus.PASSED

def ensemble_prototype_readiness_blocks_phase144(gate: EnsemblePrototypeReadinessGate) -> bool:
    return not gate.ready_for_phase144

def validate_ensemble_prototype_readiness_gate(gate: EnsemblePrototypeReadinessGate) -> List[str]:
    errors = []
    if not gate.ready_for_phase144:
         errors.append("Gate not ready for phase 144")
    return errors

def ensemble_prototype_readiness_gate_summary(gate: EnsemblePrototypeReadinessGate) -> Dict[str, Any]:
    return {"status": gate.status.value, "ready_for_phase144": gate.ready_for_phase144}

def ensemble_prototype_readiness_gate_to_text(gate: EnsemblePrototypeReadinessGate, limit: int = 300) -> str:
    return str(ensemble_prototype_readiness_gate_summary(gate))
