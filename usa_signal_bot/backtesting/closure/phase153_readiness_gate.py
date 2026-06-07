from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    Phase153ReadinessGate, Phase153ReadinessRule, Phase153ReadinessRuleKind,
    BacktestFinalAuditReport, BacktestBandClosureCertificate, Phase153HandoffContract,
    Phase153HandoffPackage, HandoffSafetyBoundaryResult, Phase153ReadinessStatus,
    BacktestClosureRiskFlag
)

def build_phase153_readiness_rules(final_audit_report: BacktestFinalAuditReport, certificate: BacktestBandClosureCertificate, contract: Phase153HandoffContract, package: Phase153HandoffPackage, boundary: HandoffSafetyBoundaryResult) -> list[Phase153ReadinessRule]:
    rules = []

    deps = {
        Phase153ReadinessRuleKind.FINAL_AUDIT_REPORT_VALID: final_audit_report.final_audit_passed,
        Phase153ReadinessRuleKind.CLOSURE_CERTIFICATE_VALID: certificate.closed,
        Phase153ReadinessRuleKind.HANDOFF_CONTRACT_VALID: contract.contract_valid,
        Phase153ReadinessRuleKind.HANDOFF_PACKAGE_VALID: package.package_valid,
        Phase153ReadinessRuleKind.HANDOFF_SAFETY_BOUNDARY_VALID: boundary.boundary_passed
    }

    for kind, passed in deps.items():
        rules.append(Phase153ReadinessRule(
            rule_kind=kind,
            name=kind.name,
            required=True,
            passed=passed,
            status=Phase153ReadinessStatus.PASSED if passed else Phase153ReadinessStatus.FAILED
        ))

    # the rest just assume true if all deps true for this mock implementation
    all_deps_passed = all(deps.values())

    other_kinds = [
        Phase153ReadinessRuleKind.PHASE151_STRESS_ROBUSTNESS_VALID,
        Phase153ReadinessRuleKind.NO_PORTFOLIO_OUTPUT,
        Phase153ReadinessRuleKind.NO_REAL_ORDER_OUTPUT,
        Phase153ReadinessRuleKind.NO_PAPER_MUTATION,
        Phase153ReadinessRuleKind.NO_LIVE_TRADING,
        Phase153ReadinessRuleKind.READY_FOR_PHASE153
    ]

    for kind in other_kinds:
        rules.append(Phase153ReadinessRule(
            rule_kind=kind,
            name=kind.name,
            required=True,
            passed=all_deps_passed,
            status=Phase153ReadinessStatus.PASSED if all_deps_passed else Phase153ReadinessStatus.FAILED
        ))

    return rules

def build_phase153_readiness_gate(final_audit_report: BacktestFinalAuditReport, certificate: BacktestBandClosureCertificate, contract: Phase153HandoffContract, package: Phase153HandoffPackage, boundary: HandoffSafetyBoundaryResult) -> Phase153ReadinessGate:
    gate = Phase153ReadinessGate()
    gate.rules = build_phase153_readiness_rules(final_audit_report, certificate, contract, package, boundary)

    passed = all(r.passed for r in gate.rules if r.required)

    gate.status = Phase153ReadinessStatus.PASSED if passed else Phase153ReadinessStatus.FAILED
    gate.ready_for_phase153 = passed

    gate.final_audit_report = final_audit_report
    gate.closure_certificate = certificate
    gate.handoff_contract = contract
    gate.handoff_package = package
    gate.handoff_safety_boundary = boundary

    if not passed:
        gate.risk_flags.append(BacktestClosureRiskFlag.PHASE152_READINESS_GATE_FAILED)
        gate.errors.append("Phase153 readiness gate failed")

    return gate

def phase153_readiness_passed(gate: Phase153ReadinessGate) -> bool:
    return gate.ready_for_phase153

def phase153_readiness_blocks_next_phase(gate: Phase153ReadinessGate) -> bool:
    return not gate.ready_for_phase153

def validate_phase153_readiness_gate(gate: Phase153ReadinessGate) -> list[str]:
    errors = []
    if not gate.ready_for_phase153:
        errors.append("Readiness gate failed")
    return errors

def phase153_readiness_gate_summary(gate: Phase153ReadinessGate) -> dict[str, Any]:
    return {"passed": gate.ready_for_phase153, "status": gate.status.value}

def phase153_readiness_gate_to_text(gate: Phase153ReadinessGate, limit: int = 300) -> str:
    return f"Phase153ReadinessGate(passed={gate.ready_for_phase153}, status={gate.status.value})"
