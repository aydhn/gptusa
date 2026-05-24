from typing import Dict, Any, List
import hashlib
import json
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    AdvancedFoundationFreezeItem,
    AdvancedFoundationFreezeBundle,
    ConsolidationEvidenceItem,
    AdvancedFoundationFreezeStatus,
    AdvancedFoundationFreezeDecision,
    create_foundation_freeze_item_id,
    create_foundation_freeze_id,
    _now
)

def build_advanced_foundation_freeze_items(evidence_items: List[ConsolidationEvidenceItem]) -> List[AdvancedFoundationFreezeItem]:
    items = []
    for ev in evidence_items:
        item = AdvancedFoundationFreezeItem(
            freeze_item_id=create_foundation_freeze_item_id(),
            created_at_utc=_now(),
            evidence_type=ev.evidence_type,
            source_phase=ev.source_phase,
            source_ref_id=ev.evidence_id,
            source_path=ev.source_path,
            frozen=True,
            immutable=True,
            available=ev.available,
            fresh=ev.fresh,
            stale=ev.stale
        )
        item.item_hash = stable_foundation_freeze_item_hash(vars(item))
        items.append(item)
    return items

def build_advanced_foundation_freeze_bundle(evidence_items: List[ConsolidationEvidenceItem]) -> AdvancedFoundationFreezeBundle:
    items = build_advanced_foundation_freeze_items(evidence_items)
    missing = len([i for i in items if not i.available])
    stale = len([i for i in items if i.stale])

    status = AdvancedFoundationFreezeStatus.FROZEN if missing == 0 and stale == 0 else AdvancedFoundationFreezeStatus.BLOCKED
    decision = AdvancedFoundationFreezeDecision.FREEZE_ADVANCED_FOUNDATION if missing == 0 and stale == 0 else AdvancedFoundationFreezeDecision.BLOCK

    bundle = AdvancedFoundationFreezeBundle(
        freeze_id=create_foundation_freeze_id(),
        created_at_utc=_now(),
        status=status,
        decision=decision,
        items=items,
        evidence_refs=[ev.evidence_id for ev in evidence_items],
        frozen=True,
        immutable=True,
        freeze_is_metadata_only=True,
        phase_start=101,
        phase_end=105,
        next_phase=106,
        final_phase=160,
        missing_evidence_count=missing,
        stale_evidence_count=stale
    )
    bundle.freeze_hash = stable_foundation_freeze_hash(items)
    return bundle

def stable_foundation_freeze_item_hash(payload: Dict[str, Any]) -> str:
    s = json.dumps({k: v for k, v in payload.items() if k not in ["created_at_utc", "item_hash"]}, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def stable_foundation_freeze_hash(items: List[AdvancedFoundationFreezeItem]) -> str:
    s = json.dumps([i.item_hash for i in items], sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def advanced_foundation_freeze_summary(bundle: AdvancedFoundationFreezeBundle) -> Dict[str, Any]:
    return {
        "status": bundle.status.name,
        "frozen": bundle.frozen,
        "items": len(bundle.items)
    }

def advanced_foundation_freeze_to_text(bundle: AdvancedFoundationFreezeBundle, limit: int = 200) -> str:
    return f"Foundation Freeze: {bundle.status.name}"
