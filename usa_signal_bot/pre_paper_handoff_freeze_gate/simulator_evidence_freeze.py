import hashlib
import json
from typing import Any, List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import SimulatorEvidenceFreezeStatus, SimulatorEvidenceFreezeDecision
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    SimulatorEvidenceFreezeBundle,
    SimulatorEvidenceFreezeItem,
    create_simulator_evidence_freeze_id,
    create_simulator_evidence_freeze_item_id
)
from usa_signal_bot.core.serialization import serialize_value

def required_simulator_freeze_evidence_types() -> List[str]:
    return [
        "simulator_dossier_full_review",
        "local_paper_admission_simulator_gate_dossier",
        "simulator_acceptance_seal",
        "sandbox_runtime_admission_blocker_events",
        "sandbox_runtime_admission_blocker_rules",
        "simulator_gate_full_review",
        "rehearsal_replay_result",
        "dry_admission_evidence_freeze",
        "simulator_dossier_continuity",
        "simulator_dossier_safety_report",
        "validation_reports",
        "audit_trails"
    ]

def stable_simulator_evidence_freeze_item_hash(item_payload: dict[str, Any]) -> str:
    s = json.dumps(serialize_value(item_payload), sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def stable_simulator_evidence_freeze_hash(items: List[SimulatorEvidenceFreezeItem]) -> str:
    item_hashes = sorted([i.item_hash for i in items if i.item_hash])
    s = json.dumps(item_hashes, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def build_simulator_evidence_freeze_items(payload: dict[str, Any]) -> List[SimulatorEvidenceFreezeItem]:
    items = []
    # Try to build items based on provided payload dict which simulates evidence refs
    for evidence_type in required_simulator_freeze_evidence_types():
        evidence_data = payload.get(evidence_type, {})
        available = bool(evidence_data)
        item_hash = stable_simulator_evidence_freeze_item_hash(evidence_data) if available else None

        item = SimulatorEvidenceFreezeItem(
            freeze_item_id=create_simulator_evidence_freeze_item_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            evidence_type=evidence_type,
            source_ref_id=payload.get(f"{evidence_type}_id"),
            source_path=payload.get(f"{evidence_type}_path"),
            frozen=True,
            immutable=True,
            available=available,
            fresh=available,
            stale=not available,
            item_hash=item_hash,
            risk_flags=[],
            warnings=[],
            errors=[]
        )
        if not available:
            item.errors.append(f"Missing evidence: {evidence_type}")
        items.append(item)
    return items

def build_simulator_evidence_freeze_bundle(payload: dict[str, Any]) -> SimulatorEvidenceFreezeBundle:
    items = build_simulator_evidence_freeze_items(payload)

    missing_count = sum(1 for i in items if not i.available)
    stale_count = sum(1 for i in items if i.stale)

    status = SimulatorEvidenceFreezeStatus.FROZEN if missing_count == 0 else SimulatorEvidenceFreezeStatus.PARTIAL
    decision = SimulatorEvidenceFreezeDecision.FREEZE_SIMULATOR_EVIDENCE if missing_count == 0 else SimulatorEvidenceFreezeDecision.BLOCK

    bundle = SimulatorEvidenceFreezeBundle(
        freeze_id=create_simulator_evidence_freeze_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        decision=decision,
        candidate_id=payload.get("candidate_id"),
        source_simulator_dossier_id=payload.get("simulator_dossier_id"),
        items=items,
        evidence_refs=[i.evidence_type for i in items if i.available],
        freeze_hash=stable_simulator_evidence_freeze_hash(items),
        frozen=True,
        immutable=True,
        freeze_is_metadata_only=True,
        missing_evidence_count=missing_count,
        stale_evidence_count=stale_count,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

    if missing_count > 0:
        bundle.errors.append("Missing required evidence items")
        bundle.required_followups.append("Provide all required simulator evidence")

    return bundle

def simulator_evidence_freeze_summary(bundle: SimulatorEvidenceFreezeBundle) -> dict[str, Any]:
    return {
        "status": bundle.status.value,
        "frozen": bundle.frozen,
        "missing_count": bundle.missing_evidence_count
    }

def simulator_evidence_freeze_to_text(bundle: SimulatorEvidenceFreezeBundle, limit: int = 100) -> str:
    res = f"Simulator Evidence Freeze: {bundle.freeze_id} ({bundle.status.value})\n"
    res += f"Missing: {bundle.missing_evidence_count}, Stale: {bundle.stale_evidence_count}\n"
    return res
