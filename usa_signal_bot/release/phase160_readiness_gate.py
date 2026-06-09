from typing import Any, Dict, List
from usa_signal_bot.release.phase159_models import (
    Phase160ReadinessGate,
    Phase160ReadinessRule,
    Phase160ReadinessRuleKind,
    Phase160ReadinessStatus,
    ReleaseCandidateAudit,
    FinalFreezeCertificate,
    Phase160HandoffPackage,
    FinalFreezeBoundaryResult,
    create_phase160_readiness_gate_id,
    create_phase160_readiness_rule_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_phase160_readiness_rules(
    audit: ReleaseCandidateAudit,
    certificate: FinalFreezeCertificate,
    package: Phase160HandoffPackage,
    boundary: FinalFreezeBoundaryResult
) -> List[Phase160ReadinessRule]:

    rules_def = [
        (Phase160ReadinessRuleKind.RELEASE_CANDIDATE_AUDIT_VALID, audit.audit_passed),
        (Phase160ReadinessRuleKind.FINAL_FREEZE_BOUNDARY_VALID, boundary.boundary_passed),
        (Phase160ReadinessRuleKind.FINAL_FREEZE_CERTIFICATE_VALID, certificate.frozen),
        (Phase160ReadinessRuleKind.PHASE160_HANDOFF_PACKAGE_VALID, package.package_valid),
        (Phase160ReadinessRuleKind.NO_LIVE_TRADING, not package.live_trading_enabled),
        (Phase160ReadinessRuleKind.NO_BROKER_EXECUTION, not package.broker_execution_enabled),
        (Phase160ReadinessRuleKind.NO_PAPER_MUTATION, not package.paper_trading_enabled),
        (Phase160ReadinessRuleKind.NO_REAL_ORDER, not package.real_order_creation_enabled),
        (Phase160ReadinessRuleKind.NO_DEPLOYMENT, not package.deployment_allowed)
    ]

    rules = []
    for kind, passed in rules_def:
        rules.append(Phase160ReadinessRule(
            rule_id=create_phase160_readiness_rule_id(),
            created_at_utc=generate_timestamp(),
            rule_kind=kind,
            name=kind.value,
            status=Phase160ReadinessStatus.PASSED if passed else Phase160ReadinessStatus.FAILED,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale="Derived from audit, certificate, package, boundary",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return rules

def build_phase160_readiness_gate(
    audit: ReleaseCandidateAudit,
    certificate: FinalFreezeCertificate,
    package: Phase160HandoffPackage,
    boundary: FinalFreezeBoundaryResult
) -> Phase160ReadinessGate:

    rules = build_phase160_readiness_rules(audit, certificate, package, boundary)
    passed = all(r.passed for r in rules if r.required)

    gate = Phase160ReadinessGate(
        gate_id=create_phase160_readiness_gate_id(),
        created_at_utc=generate_timestamp(),
        status=Phase160ReadinessStatus.PASSED if passed else Phase160ReadinessStatus.FAILED,
        rules=rules,
        release_candidate_audit=audit,
        final_freeze_certificate=certificate,
        phase160_handoff_package=package,
        final_freeze_boundary=boundary,
        ready_for_phase160=passed,
        research_data_only=True,
        final_delivery_handoff_only=True,
        dry_run_only=True,
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
        gate.risk_flags.append(AdvancedAcceptanceRiskFlag.PHASE159_READINESS_FAILED)

    return gate

def phase160_readiness_passed(gate: Phase160ReadinessGate) -> bool:
    return gate.ready_for_phase160

def phase160_readiness_blocks_next_phase(gate: Phase160ReadinessGate) -> bool:
    return not gate.ready_for_phase160

def validate_phase160_readiness_gate(gate: Phase160ReadinessGate) -> List[str]:
    errors = []
    if not gate.ready_for_phase160 and gate.status == Phase160ReadinessStatus.PASSED:
        errors.append("Status cannot be PASSED if not ready_for_phase160")
    if gate.live_trading_enabled:
        errors.append("live_trading_enabled must be False")
    return errors

def phase160_readiness_gate_to_text(gate: Phase160ReadinessGate, limit: int = 300) -> str:
    lines = [
        f"Phase 160 Readiness Gate: {gate.gate_id}",
        f"Ready for Phase 160: {gate.ready_for_phase160}",
        f"Status: {gate.status.value}"
    ]
    for r in gate.rules[:limit]:
        lines.append(f" - [{ 'x' if r.passed else ' ' }] {r.name}")
    return "\n".join(lines)
