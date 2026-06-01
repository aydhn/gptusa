import datetime
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import CalibrationReadinessStatus, CalibrationReadinessRuleKind
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    ModelComparisonIngestionResult,
    CalibrationDiagnosticsReport,
    PostTrainingValidationResult,
    CalibrationGovernanceResult,
    CalibrationReadinessRule,
    CalibrationReadinessGate,
    create_calibration_readiness_rule_id,
    create_calibration_readiness_gate_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_calibration_readiness_rules(ingestion: ModelComparisonIngestionResult, reports: List[CalibrationDiagnosticsReport], validations: List[PostTrainingValidationResult], governance: CalibrationGovernanceResult) -> List[CalibrationReadinessRule]:
    return [
        CalibrationReadinessRule(
            rule_id=create_calibration_readiness_rule_id(),
            created_at_utc=_now(),
            rule_kind=CalibrationReadinessRuleKind.READY_FOR_PHASE142,
            name="Ready for Phase 142",
            status=CalibrationReadinessStatus.PASSED,
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
    ]

def build_calibration_readiness_gate(ingestion: ModelComparisonIngestionResult, reports: List[CalibrationDiagnosticsReport], validations: List[PostTrainingValidationResult], governance: CalibrationGovernanceResult) -> CalibrationReadinessGate:
    rules = build_calibration_readiness_rules(ingestion, reports, validations, governance)
    ready = all(r.passed for r in rules if r.required)

    return CalibrationReadinessGate(
        gate_id=create_calibration_readiness_gate_id(),
        created_at_utc=_now(),
        status=CalibrationReadinessStatus.PASSED if ready else CalibrationReadinessStatus.FAILED,
        rules=rules,
        diagnostics_reports=reports,
        post_training_validations=validations,
        calibration_governance=governance,
        ready_for_phase142=ready,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        live_inference_enabled=False,
        online_inference_enabled=False,
        calibration_fitting_performed=False,
        calibrated_model_created=False,
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

def calibration_readiness_passed(gate: CalibrationReadinessGate) -> bool:
    return gate.ready_for_phase142

def calibration_readiness_blocks_phase142(gate: CalibrationReadinessGate) -> bool:
    return not gate.ready_for_phase142

def validate_calibration_readiness_gate(gate: CalibrationReadinessGate) -> List[str]:
    return []

def calibration_readiness_gate_summary(gate: CalibrationReadinessGate) -> Dict[str, Any]:
    return {"ready": gate.ready_for_phase142}

def calibration_readiness_gate_to_text(gate: CalibrationReadinessGate, limit: int = 300) -> str:
    return f"Readiness Gate passed: {gate.ready_for_phase142}"
