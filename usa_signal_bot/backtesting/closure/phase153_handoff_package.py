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
