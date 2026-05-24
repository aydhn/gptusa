from typing import Any
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import BoardDossierEvidenceStatus, BoardDossierRiskFlag
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    BoardDossierEvidenceItem,
    create_board_dossier_evidence_id
)
from usa_signal_bot.paper_readiness_board_dossier.non_execution_board_ingestion import (
    extract_non_execution_board,
    extract_runtime_map_replay_result,
    extract_non_execution_seal_integrity_audit,
    extract_non_execution_board_gates,
    extract_non_execution_board_assertions
)

def required_board_dossier_evidence_types() -> list[str]:
    return [
        "non_execution_board_full_review",
        "paper_readiness_non_execution_board",
        "runtime_map_replay_result",
        "non_execution_seal_integrity_audit",
        "non_execution_board_gates",
        "non_execution_board_assertions",
        "non_execution_board_continuity",
        "non_execution_board_safety_report",
        "paper_safe_dossier_full_review",
        "pre_paper_runtime_map",
        "non_execution_acceptance_seal",
        "validation_reports",
        "audit_trails"
    ]

def collect_board_dossier_evidence(board_payload: dict[str, Any]) -> list[BoardDossierEvidenceItem]:
    items = []

    board = extract_non_execution_board(board_payload)
    items.append(evidence_item_from_board_source("paper_readiness_non_execution_board", board))

    replay = extract_runtime_map_replay_result(board_payload)
    items.append(evidence_item_from_board_source("runtime_map_replay_result", replay))

    seal = extract_non_execution_seal_integrity_audit(board_payload)
    items.append(evidence_item_from_board_source("non_execution_seal_integrity_audit", seal))

    gates = extract_non_execution_board_gates(board_payload)
    items.append(evidence_item_from_board_source("non_execution_board_gates", gates))

    assertions = extract_non_execution_board_assertions(board_payload)
    items.append(evidence_item_from_board_source("non_execution_board_assertions", assertions))

    # Check for payload root object if available
    items.append(evidence_item_from_board_source("non_execution_board_full_review", board_payload))

    # Add dummies for rest to meet required list
    for t in required_board_dossier_evidence_types():
        if not any(i.evidence_type == t for i in items):
            items.append(evidence_item_from_board_source(t, None))

    return items

def evidence_item_from_board_source(evidence_type: str, source: Any | None, source_ref_id: str | None = None, source_path: str | None = None) -> BoardDossierEvidenceItem:
    available = source is not None and (not isinstance(source, list) or len(source) > 0)
    status = BoardDossierEvidenceStatus.FRESH if available else BoardDossierEvidenceStatus.MISSING

    return BoardDossierEvidenceItem(
        evidence_id=create_board_dossier_evidence_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        evidence_type=evidence_type,
        status=status,
        required=evidence_type in required_board_dossier_evidence_types(),
        available=available,
        fresh=available,
        stale=False,
        summary={"size": len(str(source))} if available else {},
        risk_flags=[BoardDossierRiskFlag.DOSSIER_EVIDENCE_MISSING] if not available else [],
        warnings=[],
        errors=[],
        source_ref_id=source_ref_id,
        source_path=source_path
    )

def board_evidence_missing_types(items: list[BoardDossierEvidenceItem]) -> list[str]:
    return [i.evidence_type for i in items if i.required and not i.available]

def board_evidence_stale_types(items: list[BoardDossierEvidenceItem]) -> list[str]:
    return [i.evidence_type for i in items if i.stale]

def board_evidence_score(items: list[BoardDossierEvidenceItem]) -> float | None:
    if not items:
        return None
    available = sum(1 for i in items if i.available)
    return available / len(items)

def board_evidence_summary(items: list[BoardDossierEvidenceItem]) -> dict[str, Any]:
    return {
        "total_items": len(items),
        "available_items": sum(1 for i in items if i.available),
        "missing_items": len(board_evidence_missing_types(items)),
        "stale_items": len(board_evidence_stale_types(items)),
        "score": board_evidence_score(items)
    }

def board_dossier_evidence_to_text(items: list[BoardDossierEvidenceItem], limit: int = 100) -> str:
    lines = [f"Board Dossier Evidence ({len(items)} items):"]
    for i, item in enumerate(items[:limit]):
        lines.append(f"  {i+1}. {item.evidence_type}: {item.status.name} (Available: {item.available})")
    if len(items) > limit:
        lines.append(f"  ... and {len(items) - limit} more")
    return "\n".join(lines)
