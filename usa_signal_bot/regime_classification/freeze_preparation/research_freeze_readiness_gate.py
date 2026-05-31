from typing import Any, Dict, List
from usa_signal_bot.core.enums import (
    ResearchFreezeReadinessRuleKind,
    ResearchFreezeReadinessStatus,
    ResearchFreezeRiskFlag
)
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    MonitoringValidationResult,
    DriftReportDocument,
    DriftReportQaRuleResult,
    ResearchFreezePackage,
    ResearchFreezeReadinessRule,
    ResearchFreezeReadinessGate,
    create_research_freeze_readiness_rule_id,
    create_research_freeze_readiness_gate_id,
    _now_utc_str
)

def build_research_freeze_readiness_rules(monitoring_validation: MonitoringValidationResult, drift_report: DriftReportDocument, qa_results: List[DriftReportQaRuleResult], package: ResearchFreezePackage) -> List[ResearchFreezeReadinessRule]:
    rules = []

    # MONITORING_VALIDATION_PASSED
    rules.append(ResearchFreezeReadinessRule(
        rule_id=create_research_freeze_readiness_rule_id(),
        created_at_utc=_now_utc_str(),
        rule_kind=ResearchFreezeReadinessRuleKind.MONITORING_VALIDATION_PASSED,
        name="Monitoring Validation Passed",
        status=ResearchFreezeReadinessStatus.PASSED if monitoring_validation.validation_passed else ResearchFreezeReadinessStatus.FAILED,
        required=True,
        passed=monitoring_validation.validation_passed,
        expected_value=True,
        observed_value=monitoring_validation.validation_passed,
        rationale="Monitoring validation must pass.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # DRIFT_REPORT_QA_PASSED
    qa_passed = all(r.passed for r in qa_results)
    rules.append(ResearchFreezeReadinessRule(
        rule_id=create_research_freeze_readiness_rule_id(),
        created_at_utc=_now_utc_str(),
        rule_kind=ResearchFreezeReadinessRuleKind.DRIFT_REPORT_QA_PASSED,
        name="Drift Report QA Passed",
        status=ResearchFreezeReadinessStatus.PASSED if qa_passed else ResearchFreezeReadinessStatus.FAILED,
        required=True,
        passed=qa_passed,
        expected_value=True,
        observed_value=qa_passed,
        rationale="Drift report QA must pass.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # FREEZE_PACKAGE_COMPLETE
    rules.append(ResearchFreezeReadinessRule(
        rule_id=create_research_freeze_readiness_rule_id(),
        created_at_utc=_now_utc_str(),
        rule_kind=ResearchFreezeReadinessRuleKind.FREEZE_PACKAGE_COMPLETE,
        name="Freeze Package Complete",
        status=ResearchFreezeReadinessStatus.PASSED if package.package_valid else ResearchFreezeReadinessStatus.FAILED,
        required=True,
        passed=package.package_valid,
        expected_value=True,
        observed_value=package.package_valid,
        rationale="Freeze package must be valid.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # SAFETY_BOUNDARY_VALID
    safety_passed = not (package.produces_trade_signal or package.produces_order_decision or package.investment_advice or package.model_training_used)
    rules.append(ResearchFreezeReadinessRule(
        rule_id=create_research_freeze_readiness_rule_id(),
        created_at_utc=_now_utc_str(),
        rule_kind=ResearchFreezeReadinessRuleKind.SAFETY_BOUNDARY_VALID,
        name="Safety Boundary Valid",
        status=ResearchFreezeReadinessStatus.PASSED if safety_passed else ResearchFreezeReadinessStatus.FAILED,
        required=True,
        passed=safety_passed,
        expected_value=True,
        observed_value=safety_passed,
        rationale="Safety boundaries must be respected.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    return rules

def build_research_freeze_readiness_gate(monitoring_validation: MonitoringValidationResult, drift_report: DriftReportDocument, qa_results: List[DriftReportQaRuleResult], package: ResearchFreezePackage) -> ResearchFreezeReadinessGate:
    rules = build_research_freeze_readiness_rules(monitoring_validation, drift_report, qa_results, package)
    passed = all(r.passed for r in rules if r.required)

    return ResearchFreezeReadinessGate(
        gate_id=create_research_freeze_readiness_gate_id(),
        created_at_utc=_now_utc_str(),
        status=ResearchFreezeReadinessStatus.PASSED if passed else ResearchFreezeReadinessStatus.FAILED,
        rules=rules,
        freeze_package=package,
        ready_for_phase135=passed,
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
        errors=["Not ready for phase 135"] if not passed else [],
        risk_flags=[] if passed else [ResearchFreezeRiskFlag.PHASE133_NOT_READY],
        metadata={}
    )

def research_freeze_readiness_passed(gate: ResearchFreezeReadinessGate) -> bool:
    return gate.status == ResearchFreezeReadinessStatus.PASSED

def research_freeze_readiness_blocks_phase135(gate: ResearchFreezeReadinessGate) -> bool:
    return not gate.ready_for_phase135

def validate_research_freeze_readiness_gate(gate: ResearchFreezeReadinessGate) -> List[str]:
    errors = []
    if gate.ready_for_phase135 and gate.status != ResearchFreezeReadinessStatus.PASSED:
        errors.append("Gate cannot be ready for phase 135 if not passed")
    return errors

def research_freeze_readiness_gate_summary(gate: ResearchFreezeReadinessGate) -> Dict[str, Any]:
    return {
        "gate_id": gate.gate_id,
        "status": gate.status,
        "ready": gate.ready_for_phase135
    }

def research_freeze_readiness_gate_to_text(gate: ResearchFreezeReadinessGate, limit: int = 300) -> str:
    return f"Readiness Gate {gate.gate_id} - Ready: {gate.ready_for_phase135}"[:limit]
