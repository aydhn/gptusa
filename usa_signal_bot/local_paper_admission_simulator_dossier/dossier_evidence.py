from datetime import datetime, timezone
from typing import Any
from usa_signal_bot.core.enums import SimulatorDossierEvidenceStatus, SimulatorDossierRiskFlag
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    SimulatorDossierEvidenceItem,
    create_simulator_dossier_evidence_id
)

def required_simulator_dossier_evidence_types() -> list[str]:
    return [
        "simulator_gate_full_review",
        "final_local_paper_admission_simulator_gate",
        "rehearsal_replay_result",
        "dry_admission_evidence_freeze",
        "simulator_gate_rules",
        "simulator_gate_assertions",
        "simulator_continuity",
        "simulator_safety_report",
        "dry_admission_dossier_full_review",
        "dry_admission_acceptance_seal",
        "rehearsal_blocker_events",
        "validation_reports",
        "audit_trails"
    ]

def evidence_item_from_simulator_source(
    evidence_type: str,
    source: Any | None,
    source_ref_id: str | None = None,
    source_path: str | None = None
) -> SimulatorDossierEvidenceItem:
    available = source is not None
    status = SimulatorDossierEvidenceStatus.FRESH if available else SimulatorDossierEvidenceStatus.MISSING
    fresh = available
    stale = False

    if isinstance(source, dict) and source.get("status") in ["STALE", "FAILED"]:
        status = SimulatorDossierEvidenceStatus.STALE
        fresh = False
        stale = True

    return SimulatorDossierEvidenceItem(
        evidence_id=create_simulator_dossier_evidence_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        evidence_type=evidence_type,
        status=status,
        required=evidence_type in required_simulator_dossier_evidence_types(),
        available=available,
        fresh=fresh,
        stale=stale,
        summary={"source_type": type(source).__name__ if source else "None"},
        risk_flags=[],
        warnings=[],
        errors=[],
        source_ref_id=source_ref_id,
        source_path=source_path,
        metadata={}
    )

def collect_simulator_dossier_evidence(payload: dict[str, Any]) -> list[SimulatorDossierEvidenceItem]:
    items = []
    for ev_type in required_simulator_dossier_evidence_types():
        source = payload.get(ev_type, payload.get("ingested_simulator_gate_review", {}).get(ev_type))
        item = evidence_item_from_simulator_source(ev_type, source)
        items.append(item)
    return items

def simulator_evidence_missing_types(items: list[SimulatorDossierEvidenceItem]) -> list[str]:
    return [i.evidence_type for i in items if i.required and not i.available]

def simulator_evidence_stale_types(items: list[SimulatorDossierEvidenceItem]) -> list[str]:
    return [i.evidence_type for i in items if i.stale]

def simulator_evidence_score(items: list[SimulatorDossierEvidenceItem]) -> float | None:
    if not items:
        return None
    score = sum([1.0 if i.fresh and i.available else 0.0 for i in items])
    return score / len(items)

def simulator_evidence_summary(items: list[SimulatorDossierEvidenceItem]) -> dict[str, Any]:
    return {
        "total": len(items),
        "available": len([i for i in items if i.available]),
        "fresh": len([i for i in items if i.fresh]),
        "missing": len(simulator_evidence_missing_types(items)),
        "stale": len(simulator_evidence_stale_types(items)),
        "score": simulator_evidence_score(items)
    }

def simulator_dossier_evidence_to_text(items: list[SimulatorDossierEvidenceItem], limit: int = 100) -> str:
    summary = simulator_evidence_summary(items)
    lines = [
        "--- Simulator Dossier Evidence ---",
        f"Total: {summary['total']}, Available: {summary['available']}, Missing: {summary['missing']}"
    ]
    for i in items[:limit]:
        lines.append(f"  - {i.evidence_type}: {i.status.value}")
    return "\n".join(lines)
