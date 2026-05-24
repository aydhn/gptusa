import hashlib
import json
from datetime import datetime, timezone
from typing import Any, List
from usa_signal_bot.core.enums import (
    BoardEvidenceFreezeStatus,
    BoardEvidenceFreezeDecision,
    DryAdmissionGateRiskFlag
)
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    BoardEvidenceFreezeItem,
    BoardEvidenceFreezeBundle,
    create_board_evidence_freeze_id,
    create_board_evidence_freeze_item_id
)
from usa_signal_bot.paper_mode_dry_admission_gate.board_dossier_ingestion import extract_board_dossier_candidate_id, extract_board_dossier

def required_board_freeze_evidence_types() -> List[str]:
    return [
        "board_dossier_full_review",
        "paper_readiness_board_dossier",
        "acceptance_board_seal",
        "shadow_launch_blocker_events",
        "shadow_launch_blocker_rules",
        "non_execution_board_full_review",
        "runtime_map_replay_result",
        "non_execution_seal_integrity_audit",
        "board_dossier_continuity",
        "board_dossier_safety_report",
        "validation_reports",
        "audit_trails"
    ]

def stable_board_evidence_freeze_item_hash(item_payload: dict[str, Any]) -> str:
    s = json.dumps(item_payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def stable_board_evidence_freeze_hash(items: List[BoardEvidenceFreezeItem]) -> str:
    hashes = [item.item_hash for item in items if item.item_hash]
    hashes.sort()
    s = json.dumps(hashes)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def build_board_evidence_freeze_items(board_payload: dict[str, Any]) -> List[BoardEvidenceFreezeItem]:
    items = []

    # Just mocked simulation based on payload presence
    evidence_map = {
        "board_dossier_full_review": True, # Assume root payload is it
        "paper_readiness_board_dossier": board_payload.get("board_dossier") is not None,
        "acceptance_board_seal": board_payload.get("acceptance_board_seal") is not None,
        "shadow_launch_blocker_events": len(board_payload.get("shadow_launch_blocker_events", [])) > 0,
        "shadow_launch_blocker_rules": True, # Assumed
        "non_execution_board_full_review": True, # Assumed
        "runtime_map_replay_result": True, # Assumed
        "non_execution_seal_integrity_audit": True, # Assumed
        "board_dossier_continuity": True, # Assumed
        "board_dossier_safety_report": True, # Assumed
        "validation_reports": True, # Assumed
        "audit_trails": True # Assumed
    }

    for ev_type in required_board_freeze_evidence_types():
        available = evidence_map.get(ev_type, False)

        payload_for_hash = {"type": ev_type, "available": available, "payload_id": board_payload.get("review_id", "unknown")}

        item = BoardEvidenceFreezeItem(
            freeze_item_id=create_board_evidence_freeze_item_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            evidence_type=ev_type,
            frozen=True,
            immutable=True,
            available=available,
            fresh=available,
            stale=not available,
            risk_flags=[DryAdmissionGateRiskFlag.BOARD_EVIDENCE_FREEZE_STALE] if not available else [],
            warnings=[],
            errors=[] if available else [f"Missing evidence: {ev_type}"],
            item_hash=stable_board_evidence_freeze_item_hash(payload_for_hash)
        )
        items.append(item)
    return items

def build_board_evidence_freeze_bundle(board_payload: dict[str, Any]) -> BoardEvidenceFreezeBundle:
    items = build_board_evidence_freeze_items(board_payload)

    missing_count = sum(1 for i in items if not i.available)
    stale_count = sum(1 for i in items if i.stale)

    status = BoardEvidenceFreezeStatus.FROZEN if missing_count == 0 else BoardEvidenceFreezeStatus.FAILED
    decision = BoardEvidenceFreezeDecision.FREEZE_BOARD_EVIDENCE if missing_count == 0 else BoardEvidenceFreezeDecision.REQUEST_BOARD_DOSSIER_REFRESH

    risk_flags = []
    if missing_count > 0 or stale_count > 0:
        risk_flags.append(DryAdmissionGateRiskFlag.BOARD_EVIDENCE_FREEZE_FAILED)

    candidate_id = extract_board_dossier_candidate_id(board_payload)
    dossier = extract_board_dossier(board_payload)

    return BoardEvidenceFreezeBundle(
        freeze_id=create_board_evidence_freeze_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        decision=decision,
        items=items,
        evidence_refs=[i.evidence_type for i in items],
        frozen=True,
        immutable=True,
        freeze_is_metadata_only=True,
        missing_evidence_count=missing_count,
        stale_evidence_count=stale_count,
        risk_flags=risk_flags,
        required_followups=["Refresh missing evidence"] if missing_count > 0 else [],
        warnings=[],
        errors=[],
        candidate_id=candidate_id,
        source_board_dossier_id=dossier.get("dossier_id") if dossier else None,
        freeze_hash=stable_board_evidence_freeze_hash(items)
    )

def board_evidence_freeze_summary(bundle: BoardEvidenceFreezeBundle) -> dict[str, Any]:
    return {
        "freeze_id": bundle.freeze_id,
        "status": bundle.status.value,
        "missing_evidence_count": bundle.missing_evidence_count,
        "frozen": bundle.frozen,
        "hash": bundle.freeze_hash
    }

def board_evidence_freeze_to_text(bundle: BoardEvidenceFreezeBundle, limit: int = 100) -> str:
    summary = board_evidence_freeze_summary(bundle)
    return f"Board Evidence Freeze {summary['freeze_id']} - Status: {summary['status']} - Missing: {summary['missing_evidence_count']}"
