from typing import Any

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    AdvancedMLAcceptanceGate,
    AdvancedMLAcceptanceRule,
    AdvancedMLAcceptanceRuleKind,
    AdvancedMLAcceptanceStatus,
    ExplainabilityReport,
    MLGovernanceClosureResult,
    AdvancedMLArtifactLineage,
    AdvancedMLFinalAuditResult,
    NonActivationMLClosureBoundaryResult,
    FinalMLModelCardClosure,
    create_advanced_ml_acceptance_rule_id,
    create_advanced_ml_acceptance_gate_id,
    current_time
)

def build_advanced_ml_acceptance_rules(
    explainability_report: ExplainabilityReport,
    governance: MLGovernanceClosureResult,
    lineage: AdvancedMLArtifactLineage,
    final_audit: AdvancedMLFinalAuditResult,
    boundary: NonActivationMLClosureBoundaryResult,
    card_closure: FinalMLModelCardClosure
) -> list[AdvancedMLAcceptanceRule]:

    rules = []

    # FINAL_AUDIT_VALID
    passed = final_audit.audit_passed
    rules.append(AdvancedMLAcceptanceRule(
        rule_id=create_advanced_ml_acceptance_rule_id(),
        created_at_utc=current_time(),
        rule_kind=AdvancedMLAcceptanceRuleKind.FINAL_AUDIT_VALID,
        name="Final Audit Valid Check",
        status=AdvancedMLAcceptanceStatus.PASSED if passed else AdvancedMLAcceptanceStatus.FAILED,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale="Final audit must pass",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # NON_ACTIVATION_BOUNDARY_VALID
    passed = boundary.boundary_passed
    rules.append(AdvancedMLAcceptanceRule(
        rule_id=create_advanced_ml_acceptance_rule_id(),
        created_at_utc=current_time(),
        rule_kind=AdvancedMLAcceptanceRuleKind.NON_ACTIVATION_BOUNDARY_VALID,
        name="Non-Activation Boundary Valid Check",
        status=AdvancedMLAcceptanceStatus.PASSED if passed else AdvancedMLAcceptanceStatus.FAILED,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale="Boundary check must pass",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    return rules

def build_advanced_ml_acceptance_gate(
    explainability_report: ExplainabilityReport,
    governance: MLGovernanceClosureResult,
    lineage: AdvancedMLArtifactLineage,
    final_audit: AdvancedMLFinalAuditResult,
    boundary: NonActivationMLClosureBoundaryResult,
    card_closure: FinalMLModelCardClosure
) -> AdvancedMLAcceptanceGate:

    rules = build_advanced_ml_acceptance_rules(
        explainability_report, governance, lineage, final_audit, boundary, card_closure
    )

    passed = all(r.passed for r in rules if r.required)

    return AdvancedMLAcceptanceGate(
        gate_id=create_advanced_ml_acceptance_gate_id(),
        created_at_utc=current_time(),
        status=AdvancedMLAcceptanceStatus.PASSED if passed else AdvancedMLAcceptanceStatus.FAILED,
        rules=rules,
        explainability_report=explainability_report,
        governance_closure=governance,
        artifact_lineage=lineage,
        final_audit=final_audit,
        non_activation_boundary=boundary,
        final_model_card_closure=card_closure,
        ready_for_phase146=passed,
        phase136_to_145_closed=passed,
        research_data_only=True,
        offline_ml_research_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        live_inference_enabled=False,
        live_monitoring_enabled=False,
        backtest_executed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def advanced_ml_acceptance_passed(gate: AdvancedMLAcceptanceGate) -> bool:
    return gate.status == AdvancedMLAcceptanceStatus.PASSED

def advanced_ml_acceptance_blocks_phase146(gate: AdvancedMLAcceptanceGate) -> bool:
    return not gate.ready_for_phase146

def validate_advanced_ml_acceptance_gate(gate: AdvancedMLAcceptanceGate) -> list[str]:
    errors = []
    if gate.ready_for_phase146 and not advanced_ml_acceptance_passed(gate):
        errors.append("Gate marked ready_for_phase146 but gate did not pass")
    if gate.activation_allowed or gate.deployment_allowed:
        errors.append("Gate allows activation or deployment")
    if gate.backtest_executed:
        errors.append("Gate indicates backtest executed in Phase 145")
    return errors

def advanced_ml_acceptance_gate_summary(gate: AdvancedMLAcceptanceGate) -> dict[str, Any]:
    return {
        "status": gate.status.value,
        "ready_for_phase146": gate.ready_for_phase146,
        "phase136_to_145_closed": gate.phase136_to_145_closed
    }

def advanced_ml_acceptance_gate_to_text(gate: AdvancedMLAcceptanceGate, limit: int = 300) -> str:
    summary = advanced_ml_acceptance_gate_summary(gate)
    return f"Acceptance Gate Status: {summary['status']}. Ready for Phase 146: {summary['ready_for_phase146']}"
