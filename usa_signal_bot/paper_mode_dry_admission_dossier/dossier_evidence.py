from typing import Any
import datetime

from usa_signal_bot.core.enums import DryAdmissionDossierEvidenceStatus, DryAdmissionDossierRiskFlag
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionDossierEvidenceItem, create_dry_admission_dossier_evidence_id

def required_dry_admission_dossier_evidence_types() -> list[str]:
    return [
        "dry_admission_gate_full_review",
        "final_paper_mode_dry_admission_gate",
        "shadow_launch_replay_result",
        "board_evidence_freeze",
        "dry_admission_rules",
        "dry_admission_assertions",
        "dry_admission_continuity",
        "dry_admission_safety_report",
        "board_dossier_full_review",
        "acceptance_board_seal",
        "shadow_launch_blocker_events",
        "validation_reports",
        "audit_trails"
    ]

def evidence_item_from_dry_admission_source(
    evidence_type: str,
    source: Any | None,
    source_ref_id: str | None = None,
    source_path: str | None = None
) -> DryAdmissionDossierEvidenceItem:
    now = datetime.datetime.utcnow().isoformat() + "Z"

    available = source is not None
    status = DryAdmissionDossierEvidenceStatus.FRESH if available else DryAdmissionDossierEvidenceStatus.MISSING

    if available and isinstance(source, dict) and source.get("status") in ["STALE", "FAILED"]:
        status = DryAdmissionDossierEvidenceStatus.STALE if source.get("status") == "STALE" else DryAdmissionDossierEvidenceStatus.FAILED

    return DryAdmissionDossierEvidenceItem(
        evidence_id=create_dry_admission_dossier_evidence_id(),
        created_at_utc=now,
        evidence_type=evidence_type,
        source_ref_id=source_ref_id,
        source_path=source_path,
        status=status,
        required=evidence_type in required_dry_admission_dossier_evidence_types(),
        available=available,
        fresh=status == DryAdmissionDossierEvidenceStatus.FRESH,
        stale=status == DryAdmissionDossierEvidenceStatus.STALE,
        summary={"available": available, "type": evidence_type},
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={"source_extracted": True} if available else {}
    )

def collect_dry_admission_dossier_evidence(payload: dict[str, Any]) -> list[DryAdmissionDossierEvidenceItem]:
    items = []

    gate_review = payload.get("dry_admission_gate_full_review")
    items.append(evidence_item_from_dry_admission_source("dry_admission_gate_full_review", gate_review))

    final_gate = payload.get("final_dry_admission_gate")
    items.append(evidence_item_from_dry_admission_source("final_paper_mode_dry_admission_gate", final_gate))

    shadow_replay = payload.get("shadow_replay_result")
    items.append(evidence_item_from_dry_admission_source("shadow_launch_replay_result", shadow_replay))

    freeze = payload.get("board_evidence_freeze")
    items.append(evidence_item_from_dry_admission_source("board_evidence_freeze", freeze))

    rules = payload.get("dry_admission_rules")
    items.append(evidence_item_from_dry_admission_source("dry_admission_rules", rules))

    assertions = payload.get("dry_admission_assertions")
    items.append(evidence_item_from_dry_admission_source("dry_admission_assertions", assertions))

    # Add empty placeholders for other required types to ensure completeness
    other_types = [
        "dry_admission_continuity",
        "dry_admission_safety_report",
        "board_dossier_full_review",
        "acceptance_board_seal",
        "shadow_launch_blocker_events",
        "validation_reports",
        "audit_trails"
    ]

    for t in other_types:
        source = payload.get(t)
        items.append(evidence_item_from_dry_admission_source(t, source))

    return items

def dry_admission_evidence_missing_types(items: list[DryAdmissionDossierEvidenceItem]) -> list[str]:
    return [item.evidence_type for item in items if item.required and not item.available]

def dry_admission_evidence_stale_types(items: list[DryAdmissionDossierEvidenceItem]) -> list[str]:
    return [item.evidence_type for item in items if item.stale]

def dry_admission_evidence_score(items: list[DryAdmissionDossierEvidenceItem]) -> float | None:
    if not items:
        return 0.0

    required_items = [i for i in items if i.required]
    if not required_items:
        return 1.0

    available_required = [i for i in required_items if i.available and i.fresh]
    return len(available_required) / len(required_items)

def dry_admission_evidence_summary(items: list[DryAdmissionDossierEvidenceItem]) -> dict[str, Any]:
    return {
        "total": len(items),
        "available": sum(1 for i in items if i.available),
        "required_missing": len(dry_admission_evidence_missing_types(items)),
        "stale": len(dry_admission_evidence_stale_types(items)),
        "score": dry_admission_evidence_score(items)
    }

def dry_admission_dossier_evidence_to_text(items: list[DryAdmissionDossierEvidenceItem], limit: int = 100) -> str:
    summary = dry_admission_evidence_summary(items)
    text = f"Dry-Admission Dossier Evidence (Score: {summary['score']:.2f}):
"
    text += f"- Total: {summary['total']}, Available: {summary['available']}
"

    missing = dry_admission_evidence_missing_types(items)
    if missing:
        text += f"- Missing Required: {', '.join(missing[:limit])}
"

    return text
