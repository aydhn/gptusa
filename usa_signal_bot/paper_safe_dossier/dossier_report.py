from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PaperSafeDossierReportType
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import (
    PaperSafeDossierFullReview, create_paper_safe_dossier_full_review_id,
    PaperSafeGateDossier, NonExecutionAcceptanceSeal, PrePaperLocalRuntimeMap,
    PaperSafeDossierEvidenceItem, RuntimeComponentMapItem, RuntimeRouteMapItem,
    PaperSafeDossierAuditEntry
)
from usa_signal_bot.paper_safe_dossier.paper_safe_gate_dossier import build_paper_safe_gate_dossier
from usa_signal_bot.paper_safe_dossier.non_execution_acceptance_seal import build_non_execution_acceptance_seal
from usa_signal_bot.paper_safe_dossier.local_runtime_map import build_pre_paper_local_runtime_map
from usa_signal_bot.paper_safe_dossier.dossier_evidence import collect_paper_safe_dossier_evidence
from usa_signal_bot.paper_safe_dossier.dossier_audit import (
    audit_entry_from_paper_safe_dossier,
    audit_entry_from_non_execution_seal,
    audit_entry_from_runtime_map
)

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_paper_safe_dossier_full_review(paper_safe_payload: Dict[str, Any]) -> PaperSafeDossierFullReview:
    dossier = build_paper_safe_gate_dossier(paper_safe_payload)
    evidence_items = collect_paper_safe_dossier_evidence(paper_safe_payload)
    seal = build_non_execution_acceptance_seal(paper_safe_payload, evidence_items)
    runtime_map = build_pre_paper_local_runtime_map(paper_safe_payload)

    dossier.non_execution_seal = seal
    dossier.runtime_map = runtime_map

    audit_entries = [
        audit_entry_from_paper_safe_dossier(dossier),
        audit_entry_from_non_execution_seal(seal),
        audit_entry_from_runtime_map(runtime_map)
    ]

    return PaperSafeDossierFullReview(
        review_id=create_paper_safe_dossier_full_review_id(),
        created_at_utc=utcnow_iso(),
        report_type=PaperSafeDossierReportType.FULL_PAPER_SAFE_DOSSIER_REVIEW,
        dossiers=[dossier],
        evidence_items=evidence_items,
        non_execution_seals=[seal],
        runtime_maps=[runtime_map],
        component_items=runtime_map.component_items,
        route_items=runtime_map.route_items,
        audit_entries=audit_entries,
        output_paths={},
        warnings=dossier.warnings + seal.warnings + runtime_map.warnings,
        errors=dossier.errors + seal.errors + runtime_map.errors
    )

def build_paper_safe_dossier_review_from_parts(dossier: PaperSafeGateDossier, seal: Optional[NonExecutionAcceptanceSeal] = None, runtime_map: Optional[PrePaperLocalRuntimeMap] = None) -> PaperSafeDossierFullReview:
    dossier.non_execution_seal = seal
    dossier.runtime_map = runtime_map

    audit_entries = [audit_entry_from_paper_safe_dossier(dossier)]
    if seal: audit_entries.append(audit_entry_from_non_execution_seal(seal))
    if runtime_map: audit_entries.append(audit_entry_from_runtime_map(runtime_map))

    return PaperSafeDossierFullReview(
        review_id=create_paper_safe_dossier_full_review_id(),
        created_at_utc=utcnow_iso(),
        report_type=PaperSafeDossierReportType.FULL_PAPER_SAFE_DOSSIER_REVIEW,
        dossiers=[dossier],
        evidence_items=dossier.evidence_items,
        non_execution_seals=[seal] if seal else [],
        runtime_maps=[runtime_map] if runtime_map else [],
        component_items=runtime_map.component_items if runtime_map else [],
        route_items=runtime_map.route_items if runtime_map else [],
        audit_entries=audit_entries,
        output_paths={},
        warnings=dossier.warnings + (seal.warnings if seal else []) + (runtime_map.warnings if runtime_map else []),
        errors=dossier.errors + (seal.errors if seal else []) + (runtime_map.errors if runtime_map else [])
    )

def paper_safe_dossier_full_review_summary(review: PaperSafeDossierFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "report_type": review.report_type.value,
        "dossiers": len(review.dossiers),
        "seals": len(review.non_execution_seals),
        "runtime_maps": len(review.runtime_maps),
        "errors": len(review.errors)
    }

def paper_safe_dossier_limitations_text() -> str:
    return """LIMITATIONS:
- This is a local metadata report only.
- No broker/live/demo order will be created.
- No active paper enable will be triggered.
- No paper admission will occur.
- No real paper state mutation is allowed.
- No paper order is generated.
- No Telegram real send will be dispatched.
- No production config patch will be applied.
- Paper-safe dossier IS NOT activation.
- Non-execution seal IS metadata-only.
- Pre-paper local runtime map IS metadata-only.
- NOT INVESTMENT ADVICE."""

def paper_safe_dossier_full_review_to_text(review: PaperSafeDossierFullReview, limit: int = 100) -> str:
    lines = [
        f"Paper Safe Dossier Full Review: {review.review_id}",
        f"Dossiers: {len(review.dossiers)} | Seals: {len(review.non_execution_seals)} | Runtime Maps: {len(review.runtime_maps)}",
        f"Errors: {len(review.errors)} | Warnings: {len(review.warnings)}",
        "",
        paper_safe_dossier_limitations_text()
    ]
    return "\n".join(lines)
