from typing import Any, Dict, List
from .phase142_models import (
    EnsembleReadinessGate,
    EnsembleReadinessRule,
    CalibrationDiagnosticsIngestionResult,
    EnsemblePreparationReport,
    EnsembleGovernanceResult,
    NonActivationEnsembleBoundaryResult,
    EnsembleReadinessRuleKind,
    EnsembleReadinessStatus,
    create_ensemble_readiness_rule_id,
    create_ensemble_readiness_gate_id,
    validate_ensemble_readiness_gate,
    _now
)

def build_ensemble_readiness_rules(
    ingestion: CalibrationDiagnosticsIngestionResult,
    reports: List[EnsemblePreparationReport],
    governance: EnsembleGovernanceResult,
    boundary: NonActivationEnsembleBoundaryResult
) -> List[EnsembleReadinessRule]:

    rules = []
    r1 = EnsembleReadinessRule(
        rule_id=create_ensemble_readiness_rule_id(),
        created_at_utc=_now(),
        rule_kind=EnsembleReadinessRuleKind.ENSEMBLE_GOVERNANCE_VALID,
        name="Ensemble Governance Valid",
        status=EnsembleReadinessStatus.PASSED if governance.governance_passed else EnsembleReadinessStatus.FAILED,
        required=True,
        passed=governance.governance_passed,
        expected_value=True,
        observed_value=governance.governance_passed,
        rationale="Must pass governance",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    rules.append(r1)

    r2 = EnsembleReadinessRule(
        rule_id=create_ensemble_readiness_rule_id(),
        created_at_utc=_now(),
        rule_kind=EnsembleReadinessRuleKind.NON_ACTIVATION_BOUNDARY_VALID,
        name="Non-Activation Boundary Valid",
        status=EnsembleReadinessStatus.PASSED if boundary.boundary_passed else EnsembleReadinessStatus.FAILED,
        required=True,
        passed=boundary.boundary_passed,
        expected_value=True,
        observed_value=boundary.boundary_passed,
        rationale="Must pass boundary",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    rules.append(r2)
    return rules

def build_ensemble_readiness_gate(
    ingestion: CalibrationDiagnosticsIngestionResult,
    reports: List[EnsemblePreparationReport],
    governance: EnsembleGovernanceResult,
    boundary: NonActivationEnsembleBoundaryResult
) -> EnsembleReadinessGate:

    rules = build_ensemble_readiness_rules(ingestion, reports, governance, boundary)
    passed = all(r.passed for r in rules if r.required)

    gate = EnsembleReadinessGate(
        gate_id=create_ensemble_readiness_gate_id(),
        created_at_utc=_now(),
        status=EnsembleReadinessStatus.PASSED if passed else EnsembleReadinessStatus.FAILED,
        rules=rules,
        preparation_reports=reports,
        ensemble_governance=governance,
        non_activation_boundary=boundary,
        ready_for_phase143=passed,
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

    val_errs = validate_ensemble_readiness_gate(gate)
    if val_errs:
        gate.ready_for_phase143 = False
        gate.status = EnsembleReadinessStatus.FAILED
        gate.errors.extend(val_errs)

    return gate

def ensemble_readiness_passed(gate: EnsembleReadinessGate) -> bool:
    return gate.ready_for_phase143

def ensemble_readiness_blocks_phase143(gate: EnsembleReadinessGate) -> bool:
    return not gate.ready_for_phase143

def ensemble_readiness_gate_summary(gate: EnsembleReadinessGate) -> Dict[str, Any]:
    return {"ready": gate.ready_for_phase143}

def ensemble_readiness_gate_to_text(gate: EnsembleReadinessGate, limit: int = 300) -> str:
    return f"Readiness Passed: {gate.ready_for_phase143}"
