import hashlib
import json
from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderExpansionFreezeBundle,
    ProviderFreezeEvidenceItem,
    create_provider_expansion_freeze_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import ProviderFreezeStatus, ProviderFreezeRiskFlag
from usa_signal_bot.provider_freeze.freeze_evidence_collector import missing_freeze_evidence

def build_provider_expansion_freeze_bundle(evidence_items: List[ProviderFreezeEvidenceItem]) -> ProviderExpansionFreezeBundle:
    bundle = ProviderExpansionFreezeBundle(
        freeze_id=create_provider_expansion_freeze_id(),
        created_at_utc=_utcnow_str(),
        evidence_items=evidence_items,
        total_items=len(evidence_items)
    )

    missing = missing_freeze_evidence(evidence_items)
    bundle.missing_items = len(missing)
    if missing:
        bundle.warnings.append(f"Missing required evidence: {', '.join(missing)}")
        bundle.risk_flags.append(ProviderFreezeRiskFlag.FREEZE_EVIDENCE_MISSING)

    for item in evidence_items:
        if item.frozen:
            bundle.frozen_items += 1
        if item.stale:
            bundle.stale_items += 1
            bundle.risk_flags.append(ProviderFreezeRiskFlag.FREEZE_ITEM_STALE)
        if not item.valid:
            bundle.invalid_items += 1
        if item.contains_secret:
            bundle.secret_violation_count += 1
            bundle.risk_flags.append(ProviderFreezeRiskFlag.SECRET_LEAK_RISK)
        if item.contains_execution:
            bundle.execution_violation_count += 1
            bundle.risk_flags.append(ProviderFreezeRiskFlag.ORDER_RISK)
        if item.contains_trade_signal:
            bundle.trade_signal_violation_count += 1
            bundle.risk_flags.append(ProviderFreezeRiskFlag.TRADE_SIGNAL_LANGUAGE_RISK)
        if item.contains_order_decision:
            bundle.order_decision_violation_count += 1
            bundle.risk_flags.append(ProviderFreezeRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK)

    bundle.freeze_hash = stable_provider_freeze_hash(evidence_items)
    bundle.frozen = True
    bundle.immutable = True

    if (bundle.invalid_items > 0 or
        bundle.secret_violation_count > 0 or
        bundle.execution_violation_count > 0 or
        bundle.trade_signal_violation_count > 0 or
        bundle.order_decision_violation_count > 0):
        bundle.freeze_valid = False
        bundle.status = ProviderFreezeStatus.FAILED
    else:
        bundle.freeze_valid = True
        bundle.status = ProviderFreezeStatus.FROZEN

    return bundle

def stable_provider_freeze_hash(evidence_items: List[ProviderFreezeEvidenceItem]) -> str:
    # Sort items by name for consistent hashing
    sorted_items = sorted(evidence_items, key=lambda x: x.evidence_name)
    hasher = hashlib.sha256()
    for item in sorted_items:
        # Include evidence name and its hash/status in the bundle hash
        data = f"{item.evidence_name}:{item.valid}:{item.frozen}:{item.artifact_hash or ''}"
        hasher.update(data.encode('utf-8'))
    return hasher.hexdigest()

def provider_freeze_bundle_summary(bundle: ProviderExpansionFreezeBundle) -> Dict[str, Any]:
    return {
        "freeze_id": bundle.freeze_id,
        "status": bundle.status.value,
        "valid": bundle.freeze_valid,
        "total_items": bundle.total_items,
        "missing_items": bundle.missing_items,
        "invalid_items": bundle.invalid_items,
        "secret_violations": bundle.secret_violation_count,
        "execution_violations": bundle.execution_violation_count
    }

def provider_freeze_bundle_to_text(bundle: ProviderExpansionFreezeBundle, limit: int = 300) -> str:
    lines = [
        f"Provider Expansion Freeze Bundle: {bundle.freeze_id}",
        f"Status: {bundle.status.value}, Valid: {bundle.freeze_valid}",
        f"Hash: {bundle.freeze_hash}",
        f"Items: {bundle.total_items} (Frozen: {bundle.frozen_items}, Missing: {bundle.missing_items}, Invalid: {bundle.invalid_items})",
        f"Violations - Secrets: {bundle.secret_violation_count}, Execution: {bundle.execution_violation_count}, Trade Signals: {bundle.trade_signal_violation_count}, Order Decisions: {bundle.order_decision_violation_count}"
    ]
    if bundle.warnings:
        lines.append("Warnings:")
        for w in bundle.warnings[:limit]:
            lines.append(f" - {w}")
    if bundle.errors:
        lines.append("Errors:")
        for e in bundle.errors[:limit]:
            lines.append(f" - {e}")
    return "\n".join(lines)
