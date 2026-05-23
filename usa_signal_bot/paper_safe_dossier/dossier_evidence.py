from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PaperSafeDossierEvidenceStatus, PaperSafeDossierRiskFlag
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PaperSafeDossierEvidenceItem, create_paper_safe_dossier_evidence_id
from usa_signal_bot.paper_safe_dossier.paper_safe_ingestion import (
    extract_final_paper_safe_gate,
    extract_boundary_replay_result,
    extract_frozen_evidence_integrity_audit,
    extract_paper_safe_rules,
    extract_paper_safe_assertions
)

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def required_paper_safe_dossier_evidence_types() -> List[str]:
    return [
        "paper_safe_gate_full_review",
        "final_paper_safe_gate",
        "boundary_replay_result",
        "frozen_evidence_integrity_audit",
        "paper_safe_rules",
        "paper_safe_assertions",
        "paper_safe_continuity",
        "paper_safe_safety_report",
        "boundary_certificate_full_review",
        "no_order_dossier_full_review",
        "bridge_full_review",
        "validation_reports",
        "audit_trails"
    ]

def collect_paper_safe_dossier_evidence(paper_safe_payload: Dict[str, Any]) -> List[PaperSafeDossierEvidenceItem]:
    items = []

    # 1. Full Review
    if paper_safe_payload:
         items.append(evidence_item_from_paper_safe_source("paper_safe_gate_full_review", paper_safe_payload, paper_safe_payload.get("review_id")))
    else:
         items.append(evidence_item_from_paper_safe_source("paper_safe_gate_full_review", None))

    # 2. Final Gate
    gate = extract_final_paper_safe_gate(paper_safe_payload)
    if gate:
        items.append(evidence_item_from_paper_safe_source("final_paper_safe_gate", gate, gate.get("gate_id")))
    else:
        items.append(evidence_item_from_paper_safe_source("final_paper_safe_gate", None))

    # 3. Boundary Replay Result
    replay = extract_boundary_replay_result(paper_safe_payload)
    if replay:
        items.append(evidence_item_from_paper_safe_source("boundary_replay_result", replay, replay.get("replay_result_id")))
    else:
         items.append(evidence_item_from_paper_safe_source("boundary_replay_result", None))

    # 4. Integrity Audit
    audit = extract_frozen_evidence_integrity_audit(paper_safe_payload)
    if audit:
         items.append(evidence_item_from_paper_safe_source("frozen_evidence_integrity_audit", audit, audit.get("audit_id")))
    else:
         items.append(evidence_item_from_paper_safe_source("frozen_evidence_integrity_audit", None))

    # 5. Rules
    rules = extract_paper_safe_rules(paper_safe_payload)
    if rules:
        items.append(evidence_item_from_paper_safe_source("paper_safe_rules", rules))
    else:
        items.append(evidence_item_from_paper_safe_source("paper_safe_rules", None))

    # 6. Assertions
    assertions = extract_paper_safe_assertions(paper_safe_payload)
    if assertions:
        items.append(evidence_item_from_paper_safe_source("paper_safe_assertions", assertions))
    else:
        items.append(evidence_item_from_paper_safe_source("paper_safe_assertions", None))

    # Add dummies for the rest
    for t in required_paper_safe_dossier_evidence_types()[6:]:
         items.append(evidence_item_from_paper_safe_source(t, None))

    return items

def evidence_item_from_paper_safe_source(evidence_type: str, source: Any | None, source_ref_id: Optional[str] = None, source_path: Optional[str] = None) -> PaperSafeDossierEvidenceItem:
    available = source is not None
    required = evidence_type in required_paper_safe_dossier_evidence_types()
    status = PaperSafeDossierEvidenceStatus.FRESH if available else PaperSafeDossierEvidenceStatus.MISSING

    return PaperSafeDossierEvidenceItem(
        evidence_id=create_paper_safe_dossier_evidence_id(),
        created_at_utc=utcnow_iso(),
        evidence_type=evidence_type,
        source_ref_id=source_ref_id,
        source_path=source_path,
        status=status,
        required=required,
        available=available,
        fresh=available,
        stale=not available,
        summary={"available": available, "type": type(source).__name__ if available else "None"},
        risk_flags=[PaperSafeDossierRiskFlag.DOSSIER_EVIDENCE_MISSING] if required and not available else [],
        warnings=[],
        errors=[]
    )

def paper_safe_evidence_missing_types(items: List[PaperSafeDossierEvidenceItem]) -> List[str]:
    return [i.evidence_type for i in items if i.required and not i.available]

def paper_safe_evidence_stale_types(items: List[PaperSafeDossierEvidenceItem]) -> List[str]:
    return [i.evidence_type for i in items if i.available and i.stale]

def paper_safe_evidence_score(items: List[PaperSafeDossierEvidenceItem]) -> Optional[float]:
    if not items:
        return None
    required_items = [i for i in items if i.required]
    if not required_items:
        return 100.0
    fresh_items = [i for i in required_items if i.available and i.fresh]
    return (len(fresh_items) / len(required_items)) * 100.0

def paper_safe_evidence_summary(items: List[PaperSafeDossierEvidenceItem]) -> Dict[str, Any]:
    return {
        "total": len(items),
        "available": len([i for i in items if i.available]),
        "missing": len(paper_safe_evidence_missing_types(items)),
        "stale": len(paper_safe_evidence_stale_types(items)),
        "score": paper_safe_evidence_score(items)
    }

def paper_safe_dossier_evidence_to_text(items: List[PaperSafeDossierEvidenceItem], limit: int = 100) -> str:
    summary = paper_safe_evidence_summary(items)
    lines = [
        f"Evidence Score: {summary['score']:.2f}%",
        f"Total: {summary['total']} | Available: {summary['available']} | Missing: {summary['missing']}"
    ]
    for i, item in enumerate(items[:limit]):
        lines.append(f" - {item.evidence_type}: {item.status.value}")
    if len(items) > limit:
         lines.append(f" - ... and {len(items)-limit} more.")
    return "\n".join(lines)
