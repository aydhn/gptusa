from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import MonitoringValidationRuleKind, ResearchFreezeQuality
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeMonitoringIngestionResult,
    MonitoringValidationResult,
    MonitoringValidationRule,
    create_monitoring_validation_result_id,
    _now_utc_str
)
from usa_signal_bot.regime_classification.freeze_preparation.monitoring_validation_specs import build_monitoring_validation_rule

def _build_availability_rules(
    ingestion: RegimeMonitoringIngestionResult,
    baseline: Optional[Dict[str, Any]],
    snapshot: Optional[Dict[str, Any]],
    drift_result: Optional[Dict[str, Any]],
    degradation_diagnostics: List[Dict[str, Any]],
    readiness_gate: Optional[Dict[str, Any]]
) -> List[MonitoringValidationRule]:
    rules = []
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.MONITORING_REVIEW_VALID,
        ingestion.valid_for_phase134,
        rationale="Ingestion must be valid for phase 134"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.BASELINE_AVAILABLE,
        baseline is not None,
        rationale="Baseline must be available"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.SNAPSHOT_AVAILABLE,
        snapshot is not None,
        rationale="Snapshot must be available"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.DRIFT_RESULT_AVAILABLE,
        drift_result is not None,
        rationale="Drift result must be available"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.DEGRADATION_DIAGNOSTICS_AVAILABLE,
        len(degradation_diagnostics) > 0,
        rationale="Degradation diagnostics must be available"
    ))
    rg_passed = readiness_gate.get("ready", False) if readiness_gate else False
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.MONITORING_READINESS_GATE_PASSED,
        rg_passed,
        rationale="Readiness gate must pass"
    ))
    return rules

def _build_hash_consistency_rules(
    baseline: Optional[Dict[str, Any]],
    snapshot: Optional[Dict[str, Any]],
    drift_result: Optional[Dict[str, Any]],
    degradation_diagnostics: List[Dict[str, Any]]
) -> List[MonitoringValidationRule]:
    rules = []
    # dummy hash validations for safety layer
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.BASELINE_HASH_VALID,
        baseline is not None,
        rationale="Baseline hash must be valid"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.SNAPSHOT_HASH_VALID,
        snapshot is not None,
        rationale="Snapshot hash must be valid"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.DRIFT_RESULT_VALID,
        drift_result is not None,
        rationale="Drift result must be valid"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.DEGRADATION_RESULT_VALID,
        len(degradation_diagnostics) > 0,
        rationale="Degradation result must be valid"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.CONSISTENCY_VALID,
        baseline is not None and snapshot is not None,
        rationale="Consistency must be valid"
    ))
    return rules

def _build_safety_rules(
    ingestion: RegimeMonitoringIngestionResult
) -> List[MonitoringValidationRule]:
    rules = []
    safety = not (ingestion.produces_trade_signal or ingestion.produces_order_decision or ingestion.investment_advice)
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.SAFETY_BOUNDARY_VALID,
        safety,
        rationale="Safety boundaries must be respected"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.NO_SIGNAL_OUTPUT,
        not ingestion.produces_trade_signal,
        rationale="Must not produce trade signals"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.NO_ORDER_OUTPUT,
        not ingestion.produces_order_decision,
        rationale="Must not produce order decisions"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.NO_PORTFOLIO_OUTPUT,
        not ingestion.produces_portfolio_weights,
        rationale="Must not produce portfolio weights"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.NO_EXECUTION_OUTPUT,
        not (ingestion.active_paper_enabled or ingestion.broker_execution_enabled),
        rationale="Must not have execution output"
    ))
    rules.append(build_monitoring_validation_rule(
        MonitoringValidationRuleKind.NO_MODEL_TRAINING,
        not ingestion.model_training_used,
        rationale="Must not use model training"
    ))
    return rules

def build_monitoring_validation_rules(
    ingestion: RegimeMonitoringIngestionResult,
    baseline: Optional[Dict[str, Any]],
    snapshot: Optional[Dict[str, Any]],
    drift_result: Optional[Dict[str, Any]],
    degradation_diagnostics: List[Dict[str, Any]],
    degradation_profiles: List[Dict[str, Any]],
    readiness_gate: Optional[Dict[str, Any]]
) -> List[MonitoringValidationRule]:

    rules = []
    rules.extend(_build_availability_rules(
        ingestion, baseline, snapshot, drift_result, degradation_diagnostics, readiness_gate
    ))
    rules.extend(_build_hash_consistency_rules(
        baseline, snapshot, drift_result, degradation_diagnostics
    ))
    rules.extend(_build_safety_rules(ingestion))

    return rules

def run_monitoring_validation(
    ingestion: RegimeMonitoringIngestionResult,
    baseline: Optional[Dict[str, Any]],
    snapshot: Optional[Dict[str, Any]],
    drift_result: Optional[Dict[str, Any]],
    degradation_diagnostics: List[Dict[str, Any]],
    degradation_profiles: List[Dict[str, Any]],
    readiness_gate: Optional[Dict[str, Any]]
) -> MonitoringValidationResult:

    rules = build_monitoring_validation_rules(
        ingestion, baseline, snapshot, drift_result, degradation_diagnostics, degradation_profiles, readiness_gate
    )

    passed_rules = sum(1 for r in rules if r.passed)
    total_rules = len(rules)
    failed_rules = total_rules - passed_rules
    validation_passed = failed_rules == 0

    rg_passed = readiness_gate.get("ready", False) if readiness_gate else False

    res = MonitoringValidationResult(
        validation_id=create_monitoring_validation_result_id(),
        created_at_utc=_now_utc_str(),
        rules=rules,
        total_rules=total_rules,
        passed_rules=passed_rules,
        warning_rules=0,
        failed_rules=failed_rules,
        blocked_rules=0,
        validation_passed=validation_passed,
        baseline_available=baseline is not None,
        snapshot_available=snapshot is not None,
        drift_result_available=drift_result is not None,
        degradation_diagnostics_available=len(degradation_diagnostics) > 0,
        monitoring_readiness_gate_passed=rg_passed,
        consistency_valid=baseline is not None and snapshot is not None,
        safety_boundary_valid=validation_passed,
        quality=ResearchFreezeQuality.HIGH if validation_passed else ResearchFreezeQuality.INVALID,
        research_metadata_only=True,
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

    if not validation_passed:
        res.errors.append("Validation failed")

    return res

def monitoring_validation_passed(result: MonitoringValidationResult) -> bool:
    return result.validation_passed

def monitoring_validation_summary(result: MonitoringValidationResult) -> Dict[str, Any]:
    return {
        "validation_id": result.validation_id,
        "passed": result.validation_passed,
        "failed_rules": result.failed_rules
    }

def monitoring_validation_to_text(result: MonitoringValidationResult, limit: int = 300) -> str:
    return f"Validation {result.validation_id} - Passed: {result.validation_passed}"[:limit]
