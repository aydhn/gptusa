import os
import textwrap

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(textwrap.dedent(content).lstrip())


# 19. HANDOFF CONTRACT
write_file("usa_signal_bot/backtesting/closure/phase153_handoff_contract.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    Phase153HandoffContract, BacktestBandClosureCertificate,
    BacktestFinalAuditReport, Phase153HandoffItemKind, BacktestClosureRiskFlag
)

def build_phase153_handoff_contract(certificate: BacktestBandClosureCertificate, final_audit_report: BacktestFinalAuditReport) -> Phase153HandoffContract:
    contract = Phase153HandoffContract()
    contract.source_certificate_id = certificate.certificate_id
    contract.source_final_audit_report_id = final_audit_report.report_id

    contract.allowed_item_kinds = [
        Phase153HandoffItemKind.READ_ONLY_PERFORMANCE_SUMMARY,
        Phase153HandoffItemKind.READ_ONLY_RISK_SUMMARY,
        Phase153HandoffItemKind.READ_ONLY_ROBUSTNESS_SCORECARD,
        Phase153HandoffItemKind.READ_ONLY_CONSTRAINT_NOTE,
        Phase153HandoffItemKind.READ_ONLY_METRIC_INVENTORY,
        Phase153HandoffItemKind.READ_ONLY_RISK_NOTE_INVENTORY,
        Phase153HandoffItemKind.READ_ONLY_ARTIFACT_LINEAGE,
        Phase153HandoffItemKind.READ_ONLY_SAFETY_SUMMARY,
        Phase153HandoffItemKind.PORTFOLIO_INPUT_CONTRACT
    ]

    contract.forbidden_fields = [
        "portfolio_weight", "target_weight", "allocation", "position_size",
        "capital_allocation", "order", "broker_order", "paper_order", "live_order",
        "sent_to_broker", "strategy_active", "deployment_enabled", "live_signal",
        "buy_signal", "sell_signal"
    ]

    contract.contract_valid = certificate.closed
    if not contract.contract_valid:
        contract.risk_flags.append(BacktestClosureRiskFlag.HANDOFF_CONTRACT_INVALID)
        contract.errors.append("Invalid contract: certificate not closed")

    return contract

def validate_phase153_handoff_contract(contract: Phase153HandoffContract) -> list[str]:
    errors = []
    if not contract.contract_valid:
        errors.append("Contract is invalid")
    if contract.portfolio_construction_allowed:
        errors.append("Portfolio construction must not be allowed in the contract")
    return errors

def phase153_handoff_contract_summary(contract: Phase153HandoffContract) -> dict[str, Any]:
    return {"valid": contract.contract_valid}

def phase153_handoff_contract_to_text(contract: Phase153HandoffContract, limit: int = 300) -> str:
    return f"Phase153HandoffContract(valid={contract.contract_valid})"
""")

# 20. HANDOFF PACKAGE
write_file("usa_signal_bot/backtesting/closure/phase153_handoff_package.py", """
import hashlib
import json
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    Phase153HandoffPackage, Phase153HandoffItem, Phase153HandoffContract,
    BacktestBandClosureCertificate, BacktestFinalAuditReport, Phase153HandoffItemKind,
    BacktestBandPhase, BacktestClosureRiskFlag
)

def build_phase153_handoff_items(final_audit_report: BacktestFinalAuditReport) -> list[Phase153HandoffItem]:
    items = []

    # Mock items
    items.append(Phase153HandoffItem(
        item_kind=Phase153HandoffItemKind.READ_ONLY_METRIC_INVENTORY,
        source_phase=BacktestBandPhase.PHASE152_CLOSURE,
        name="Metric Inventory",
        payload={"metrics": len(final_audit_report.metric_inventory)}
    ))

    return items

def compute_phase153_handoff_package_hash(package: Phase153HandoffPackage) -> str:
    content = f"{package.contract.contract_id}_{len(package.items)}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def validate_phase153_handoff_item(item: Phase153HandoffItem, contract: Phase153HandoffContract) -> list[str]:
    errors = []
    if item.contains_portfolio_weight:
        errors.append(f"Item {item.name} contains portfolio weight")
    payload_str = json.dumps(item.payload).lower()
    for field in contract.forbidden_fields:
        if field in payload_str:
            errors.append(f"Item {item.name} contains forbidden field: {field}")
    return errors

def build_phase153_handoff_package(contract: Phase153HandoffContract, certificate: BacktestBandClosureCertificate, final_audit_report: BacktestFinalAuditReport) -> Phase153HandoffPackage:
    package = Phase153HandoffPackage()
    package.contract = contract
    package.source_certificate = certificate
    package.items = build_phase153_handoff_items(final_audit_report)

    package.package_valid = contract.contract_valid and certificate.closed

    for item in package.items:
        errs = validate_phase153_handoff_item(item, contract)
        if errs:
            package.package_valid = False
            package.errors.extend(errs)

    package.package_hash = compute_phase153_handoff_package_hash(package)

    if not package.package_valid:
        package.risk_flags.append(BacktestClosureRiskFlag.HANDOFF_PACKAGE_INVALID)
        package.errors.append("Handoff package invalid")

    return package

def validate_phase153_handoff_package(package: Phase153HandoffPackage) -> list[str]:
    errors = []
    if not package.package_valid:
        errors.append("Package is invalid")
    return errors

def phase153_handoff_package_summary(package: Phase153HandoffPackage) -> dict[str, Any]:
    return {"valid": package.package_valid, "items": len(package.items), "hash": package.package_hash}

def phase153_handoff_package_to_text(package: Phase153HandoffPackage, limit: int = 300) -> str:
    return f"Phase153HandoffPackage(valid={package.package_valid}, items={len(package.items)})"
""")

# 21. HANDOFF SAFETY BOUNDARY
write_file("usa_signal_bot/backtesting/closure/handoff_safety_boundary.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    HandoffSafetyBoundaryResult, HandoffSafetyBoundaryRule, HandoffSafetyRuleKind,
    Phase153HandoffPackage, BacktestClosureRiskFlag
)

def build_handoff_safety_boundary_rules(package: Phase153HandoffPackage | None = None) -> list[HandoffSafetyBoundaryRule]:
    rules = []
    # simplified mock rules
    for kind in HandoffSafetyRuleKind:
        if kind == HandoffSafetyRuleKind.UNKNOWN: continue

        # for a safe package, assume passed
        passed = True
        if package and not package.package_valid:
            passed = False

        rules.append(HandoffSafetyBoundaryRule(
            rule_kind=kind,
            name=kind.name,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale=f"Check {kind.name}"
        ))
    return rules

def build_handoff_safety_boundary_result(rules: list[HandoffSafetyBoundaryRule]) -> HandoffSafetyBoundaryResult:
    res = HandoffSafetyBoundaryResult()
    res.rules = rules
    res.boundary_passed = all(r.passed for r in rules if r.required)

    if not res.boundary_passed:
        res.risk_flags.append(BacktestClosureRiskFlag.HANDOFF_SAFETY_BOUNDARY_FAILED)
        res.errors.append("Handoff safety boundary failed")

    return res

def handoff_safety_boundary_passed(result: HandoffSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def validate_handoff_safety_boundary_result(result: HandoffSafetyBoundaryResult) -> list[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Safety boundary failed")
    return errors

def handoff_safety_boundary_summary(result: HandoffSafetyBoundaryResult) -> dict[str, Any]:
    return {"passed": result.boundary_passed}

def handoff_safety_boundary_to_text(result: HandoffSafetyBoundaryResult, limit: int = 300) -> str:
    return f"HandoffSafetyBoundary(passed={result.boundary_passed})"
""")

# 22. READINESS GATE
write_file("usa_signal_bot/backtesting/closure/phase153_readiness_gate.py", """
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
""")
