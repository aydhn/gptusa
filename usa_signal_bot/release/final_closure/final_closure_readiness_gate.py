from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalClosureReadinessGate,
    FinalClosureReadinessRule,
    FinalClosureReadinessRuleKind,
    FinalClosureReadinessStatus,
    FinalSystemAuditReport,
    FinalDeliveryCertificate,
    ProjectClosureReport,
    ProjectClosureManifest,
    FinalSafetyBoundaryResult,
    FinalClosureRiskFlag,
    create_final_closure_readiness_rule_id,
    create_final_closure_readiness_gate_id,
    generate_timestamp
)

def build_final_closure_readiness_rules(
    audit: FinalSystemAuditReport,
    certificate: FinalDeliveryCertificate,
    closure_report: ProjectClosureReport,
    manifest: ProjectClosureManifest,
    boundary: FinalSafetyBoundaryResult
) -> List[FinalClosureReadinessRule]:

    rules = []

    def add_rule(kind: FinalClosureReadinessRuleKind, passed: bool, rationale: str):
        status = FinalClosureReadinessStatus.PASSED if passed else FinalClosureReadinessStatus.FAILED
        rules.append(FinalClosureReadinessRule(
            rule_id=create_final_closure_readiness_rule_id(),
            created_at_utc=generate_timestamp(),
            rule_kind=kind,
            name=f"Gate {kind.value}",
            status=status,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale=rationale,
            warnings=[],
            errors=["Failed gate check"] if not passed else [],
            risk_flags=[FinalClosureRiskFlag.FINAL_SYSTEM_AUDIT_FAILED] if not passed else [],
            metadata={}
        ))

    add_rule(FinalClosureReadinessRuleKind.FINAL_SYSTEM_AUDIT_VALID, audit.audit_passed, "Audit validation")
    add_rule(FinalClosureReadinessRuleKind.FINAL_DELIVERY_CERTIFICATE_VALID, certificate.delivered, "Certificate validation")
    add_rule(FinalClosureReadinessRuleKind.PROJECT_CLOSURE_REPORT_VALID, closure_report.project_closed, "Report validation")
    add_rule(FinalClosureReadinessRuleKind.PROJECT_CLOSURE_MANIFEST_VALID, manifest.project_closed, "Manifest validation")
    add_rule(FinalClosureReadinessRuleKind.FINAL_SAFETY_BOUNDARY_VALID, boundary.boundary_passed, "Boundary validation")
    add_rule(FinalClosureReadinessRuleKind.NO_LIVE_TRADING, boundary.no_live_trading, "Safety constraint")
    add_rule(FinalClosureReadinessRuleKind.NO_BROKER_EXECUTION, boundary.no_broker_execution, "Safety constraint")
    add_rule(FinalClosureReadinessRuleKind.NO_PAPER_MUTATION, boundary.no_paper_state_mutation, "Safety constraint")
    add_rule(FinalClosureReadinessRuleKind.NO_REAL_ORDER, boundary.no_real_order_creation, "Safety constraint")
    add_rule(FinalClosureReadinessRuleKind.NO_DEPLOYMENT, boundary.no_deployment, "Safety constraint")
    add_rule(FinalClosureReadinessRuleKind.PROJECT_CLOSED, closure_report.project_closed, "Project closure state")

    return rules

def build_final_closure_readiness_gate(
    audit: FinalSystemAuditReport,
    certificate: FinalDeliveryCertificate,
    closure_report: ProjectClosureReport,
    manifest: ProjectClosureManifest,
    boundary: FinalSafetyBoundaryResult
) -> FinalClosureReadinessGate:

    rules = build_final_closure_readiness_rules(audit, certificate, closure_report, manifest, boundary)
    passed = all(r.passed for r in rules if r.required)

    status = FinalClosureReadinessStatus.PASSED if passed else FinalClosureReadinessStatus.FAILED

    gate = FinalClosureReadinessGate(
        gate_id=create_final_closure_readiness_gate_id(),
        created_at_utc=generate_timestamp(),
        status=status,
        rules=rules,
        final_audit_report=audit,
        final_delivery_certificate=certificate,
        project_closure_report=closure_report,
        project_closure_manifest=manifest,
        final_safety_boundary=boundary,
        project_closed=passed,
        research_data_only=True,
        final_closure_only=True,
        live_trading_enabled=False,
        paper_state_mutation_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        telegram_real_send_enabled=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        production_patch_allowed=False,
        network_used=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    if not passed:
        gate.errors.append("Readiness gate validation failed.")
        gate.risk_flags.append(FinalClosureRiskFlag.PROJECT_CLOSURE_MANIFEST_INVALID)

    return gate

def final_closure_readiness_passed(gate: FinalClosureReadinessGate) -> bool:
    return gate.status == FinalClosureReadinessStatus.PASSED

def final_closure_readiness_blocks_project_closure(gate: FinalClosureReadinessGate) -> bool:
    return not final_closure_readiness_passed(gate)

def validate_final_closure_readiness_gate(gate: FinalClosureReadinessGate) -> List[str]:
    errors = []
    if not final_closure_readiness_passed(gate):
        errors.append("Gate has not passed.")
        errors.extend(gate.errors)
    return errors

def final_closure_readiness_gate_to_text(gate: FinalClosureReadinessGate, limit: int = 300) -> str:
    return f"Final Closure Readiness Gate: Passed={gate.status == FinalClosureReadinessStatus.PASSED}, Status={gate.status.value}"
