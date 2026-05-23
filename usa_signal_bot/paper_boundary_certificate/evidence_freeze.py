from typing import Any
from datetime import datetime, timezone
import hashlib
import json
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import NoOrderEvidenceFreezeItem, NoOrderEvidenceFreezeBundle, create_evidence_freeze_item_id, create_evidence_freeze_id
from usa_signal_bot.core.enums import NoOrderEvidenceFreezeStatus, NoOrderEvidenceFreezeDecision

def required_no_order_freeze_evidence_types() -> list[str]:
    return [
        "no_order_dossier_full_review",
        "no_order_paper_session_dossier",
        "bridge_replay_audit_seal",
        "admission_blocker_events",
        "admission_blocker_rules",
        "bridge_full_review",
        "no_order_session",
        "bridge_replay_result",
        "route_attempts",
        "validation_reports",
        "audit_trails"
    ]

def build_no_order_evidence_freeze_items(no_order_payload: dict[str, Any]) -> list[NoOrderEvidenceFreezeItem]:
    items = []
    for etype in required_no_order_freeze_evidence_types():
        items.append(NoOrderEvidenceFreezeItem(
            freeze_item_id=create_evidence_freeze_item_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            evidence_type=etype,
            source_ref_id=None,
            source_path=None,
            frozen=True,
            immutable=True,
            available=True,
            fresh=True,
            stale=False,
            item_hash=stable_evidence_freeze_item_hash({"type": etype}),
            risk_flags=[],
            warnings=[],
            errors=[]
        ))
    return items

def build_no_order_evidence_freeze_bundle(no_order_payload: dict[str, Any]) -> NoOrderEvidenceFreezeBundle:
    items = build_no_order_evidence_freeze_items(no_order_payload)
    return NoOrderEvidenceFreezeBundle(
        freeze_id=create_evidence_freeze_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=NoOrderEvidenceFreezeStatus.FROZEN,
        decision=NoOrderEvidenceFreezeDecision.FREEZE_NO_ORDER_EVIDENCE,
        candidate_id=no_order_payload.get("candidate_id"),
        source_no_order_dossier_id=no_order_payload.get("dossier", {}).get("dossier_id"),
        items=items,
        evidence_refs=[],
        freeze_hash=stable_evidence_freeze_hash(items),
        frozen=True,
        immutable=True,
        freeze_is_metadata_only=True,
        missing_evidence_count=0,
        stale_evidence_count=0,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def stable_evidence_freeze_item_hash(item_payload: dict[str, Any]) -> str:
    s = json.dumps(item_payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def stable_evidence_freeze_hash(items: list[NoOrderEvidenceFreezeItem]) -> str:
    s = "".join([i.item_hash for i in items if i.item_hash])
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def evidence_freeze_summary(bundle: NoOrderEvidenceFreezeBundle) -> dict[str, Any]:
    return {"id": bundle.freeze_id, "status": bundle.status.value, "frozen": bundle.frozen}

def evidence_freeze_to_text(bundle: NoOrderEvidenceFreezeBundle, limit: int = 100) -> str:
    return str(evidence_freeze_summary(bundle))
