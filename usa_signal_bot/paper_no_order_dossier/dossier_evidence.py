from typing import Any
from datetime import datetime, timezone
import json
from usa_signal_bot.core.enums import NoOrderDossierEvidenceStatus
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderDossierEvidenceItem,
    create_no_order_evidence_id,
    no_order_dossier_evidence_item_to_dict
)
from usa_signal_bot.paper_no_order_dossier.bridge_ingestion import (
    extract_bridge_dry_run,
    extract_no_order_session,
    extract_bridge_replay_result,
    extract_bridge_route_attempts
)

def required_no_order_dossier_evidence_types() -> list[str]:
    return [
        "paper_sandbox_bridge_full_review",
        "bridge_dry_run",
        "no_order_paper_session",
        "bridge_replay_result",
        "bridge_replay_plan",
        "bridge_route_attempts",
        "read_only_route_validation",
        "dangerous_route_validation",
        "bridge_no_write_continuity",
        "bridge_safety_report",
        "no_write_transition_dossier",
        "admission_evidence_seal_validation",
        "validation_reports",
        "audit_trails"
    ]

def evidence_item_from_bridge_source(evidence_type: str, source: Any | None, source_ref_id: str | None = None, source_path: str | None = None) -> NoOrderDossierEvidenceItem:
    available = source is not None
    status = NoOrderDossierEvidenceStatus.FRESH if available else NoOrderDossierEvidenceStatus.MISSING

    # Check if empty dict or list
    if available and (isinstance(source, dict) and not source) or (isinstance(source, list) and not source):
        status = NoOrderDossierEvidenceStatus.MISSING
        available = False

    return NoOrderDossierEvidenceItem(
        evidence_id=create_no_order_evidence_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        evidence_type=evidence_type,
        source_ref_id=source_ref_id,
        source_path=source_path,
        status=status,
        required=evidence_type in required_no_order_dossier_evidence_types(),
        available=available,
        fresh=status == NoOrderDossierEvidenceStatus.FRESH,
        stale=status == NoOrderDossierEvidenceStatus.STALE,
        summary={"available": available},
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def collect_no_order_dossier_evidence(bridge_payload: dict[str, Any]) -> list[NoOrderDossierEvidenceItem]:
    items = []

    # 1. paper_sandbox_bridge_full_review
    items.append(evidence_item_from_bridge_source(
        "paper_sandbox_bridge_full_review",
        bridge_payload,
        bridge_payload.get("review_id")
    ))

    # 2. bridge_dry_run
    items.append(evidence_item_from_bridge_source(
        "bridge_dry_run",
        extract_bridge_dry_run(bridge_payload)
    ))

    # 3. no_order_paper_session
    items.append(evidence_item_from_bridge_source(
        "no_order_paper_session",
        extract_no_order_session(bridge_payload)
    ))

    # 4. bridge_replay_result
    items.append(evidence_item_from_bridge_source(
        "bridge_replay_result",
        extract_bridge_replay_result(bridge_payload)
    ))

    # 5. bridge_replay_plan (Mocked or extracted if present)
    items.append(evidence_item_from_bridge_source(
        "bridge_replay_plan",
        bridge_payload.get("bridge_replay_plan", {})
    ))

    # 6. bridge_route_attempts
    attempts = extract_bridge_route_attempts(bridge_payload)
    items.append(evidence_item_from_bridge_source(
        "bridge_route_attempts",
        attempts if attempts else None
    ))

    # Add other required types as missing/placeholder for now to pass full review requirement
    for t in required_no_order_dossier_evidence_types():
        if not any(i.evidence_type == t for i in items):
            # Try to find in payload
            items.append(evidence_item_from_bridge_source(
                t,
                bridge_payload.get(t)
            ))

    return items

def no_order_evidence_missing_types(items: list[NoOrderDossierEvidenceItem]) -> list[str]:
    return [i.evidence_type for i in items if i.required and not i.available]

def no_order_evidence_stale_types(items: list[NoOrderDossierEvidenceItem]) -> list[str]:
    return [i.evidence_type for i in items if i.required and i.stale]

def no_order_evidence_score(items: list[NoOrderDossierEvidenceItem]) -> float | None:
    required = [i for i in items if i.required]
    if not required:
        return 0.0
    fresh = [i for i in required if i.fresh]
    return len(fresh) / len(required)

def no_order_evidence_summary(items: list[NoOrderDossierEvidenceItem]) -> dict[str, Any]:
    return {
        "total_count": len(items),
        "required_count": len([i for i in items if i.required]),
        "available_count": len([i for i in items if i.available]),
        "missing_count": len(no_order_evidence_missing_types(items)),
        "score": no_order_evidence_score(items)
    }

def dossier_evidence_to_text(items: list[NoOrderDossierEvidenceItem], limit: int = 100) -> str:
    return json.dumps([no_order_dossier_evidence_item_to_dict(i) for i in items[:limit]], indent=2)
