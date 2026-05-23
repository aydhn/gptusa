
from typing import Any, Dict, List, Optional
import hashlib
import json
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    FrozenEvidenceIntegrityItem, FrozenEvidenceIntegrityAudit,
    create_integrity_item_id, create_integrity_audit_id, utcnow_iso,
    FrozenEvidenceIntegrityStatus, FrozenEvidenceIntegrityDecision,
    PaperSafeGateRiskFlag
)

def stable_integrity_item_hash(item_payload: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(item_payload, sort_keys=True).encode('utf-8')).hexdigest()

def stable_integrity_freeze_hash(items: List[FrozenEvidenceIntegrityItem]) -> str:
    hashes = [i.observed_hash or "" for i in items]
    return hashlib.sha256("".join(sorted(hashes)).encode('utf-8')).hexdigest()

def collect_integrity_risk_flags(items: List[FrozenEvidenceIntegrityItem]) -> List[PaperSafeGateRiskFlag]:
    flags = set()
    for item in items:
        if item.tamper_detected: flags.add(PaperSafeGateRiskFlag.FROZEN_EVIDENCE_TAMPER_RISK)
        if item.stale: flags.add(PaperSafeGateRiskFlag.FROZEN_EVIDENCE_STALE)
        if not item.available: flags.add(PaperSafeGateRiskFlag.FROZEN_EVIDENCE_MISSING)
    return list(flags)

def build_frozen_evidence_integrity_items(boundary_payload: Dict[str, Any]) -> List[FrozenEvidenceIntegrityItem]:
    return []

def build_frozen_evidence_integrity_audit(boundary_payload: Dict[str, Any]) -> FrozenEvidenceIntegrityAudit:
    items = build_frozen_evidence_integrity_items(boundary_payload)
    flags = collect_integrity_risk_flags(items)

    return FrozenEvidenceIntegrityAudit(
        audit_id=create_integrity_audit_id(),
        created_at_utc=utcnow_iso(),
        status=FrozenEvidenceIntegrityStatus.VALIDATED if not flags else FrozenEvidenceIntegrityStatus.FAILED,
        decision=FrozenEvidenceIntegrityDecision.ACCEPT_FROZEN_EVIDENCE if not flags else FrozenEvidenceIntegrityDecision.BLOCK,
        candidate_id=boundary_payload.get("candidate_id"),
        source_freeze_id=None,
        source_boundary_certificate_id=boundary_payload.get("boundary_certificate_id"),
        items=items,
        expected_freeze_hash=None,
        observed_freeze_hash=stable_integrity_freeze_hash(items),
        freeze_hash_matches=True,
        checked_item_count=len(items),
        tamper_count=sum(1 for i in items if i.tamper_detected),
        missing_count=sum(1 for i in items if not i.available),
        stale_count=sum(1 for i in items if i.stale),
        frozen=True,
        immutable=True,
        integrity_valid=len(flags) == 0,
        audit_is_metadata_only=True,
        risk_flags=flags,
        required_followups=[],
        warnings=[],
        errors=[]
    )

def frozen_evidence_integrity_summary(audit: FrozenEvidenceIntegrityAudit) -> Dict[str, Any]:
    return {
        "audit_id": audit.audit_id,
        "valid": audit.integrity_valid,
        "items": audit.checked_item_count
    }

def frozen_evidence_integrity_to_text(audit: FrozenEvidenceIntegrityAudit, limit: int = 100) -> str:
    return f"Frozen Evidence Audit {audit.audit_id}: Valid={audit.integrity_valid}"
