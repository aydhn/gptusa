from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import BoardDossierReportType
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    BoardDossierFullReview,
    PaperReadinessBoardDossier,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerEvent,
    create_board_dossier_full_review_id
)
from usa_signal_bot.paper_readiness_board_dossier.board_dossier import build_paper_readiness_board_dossier
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_audit import (
    audit_entry_from_board_dossier,
    audit_entry_from_acceptance_board_seal,
    audit_entry_from_shadow_launch_blocker_events
)
from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_blocker_rules import default_shadow_launch_blocker_rules

def build_board_dossier_full_review(board_payload: dict[str, Any]) -> BoardDossierFullReview:
    dossier = build_paper_readiness_board_dossier(board_payload)
    return build_board_dossier_review_from_parts(
        dossier,
        dossier.acceptance_board_seal,
        dossier.shadow_launch_blocker_events
    )

def build_board_dossier_review_from_parts(dossier: PaperReadinessBoardDossier, seal: AcceptanceBoardSeal | None = None, blocker_events: list[ShadowLaunchBlockerEvent] | None = None) -> BoardDossierFullReview:
    events = blocker_events or []
    rules = default_shadow_launch_blocker_rules()

    audits = [audit_entry_from_board_dossier(dossier)]
    if seal:
        audits.append(audit_entry_from_acceptance_board_seal(seal))
    if events:
        audits.append(audit_entry_from_shadow_launch_blocker_events(events))

    return BoardDossierFullReview(
        review_id=create_board_dossier_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=BoardDossierReportType.FULL_BOARD_DOSSIER_REVIEW,
        dossiers=[dossier],
        evidence_items=dossier.evidence_items,
        acceptance_board_seals=[seal] if seal else [],
        shadow_launch_blocker_rules=rules,
        shadow_launch_blocker_events=events,
        audit_entries=audits,
        output_paths={},
        warnings=[],
        errors=[]
    )

def board_dossier_full_review_summary(review: BoardDossierFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "dossier_count": len(review.dossiers),
        "evidence_count": len(review.evidence_items),
        "seal_count": len(review.acceptance_board_seals),
        "blocker_event_count": len(review.shadow_launch_blocker_events),
        "audit_count": len(review.audit_entries),
        "has_warnings": len(review.warnings) > 0
    }

def board_dossier_limitations_text() -> str:
    return """
LIMITATIONS:
- No broker API access, live orders, or demo orders.
- No active paper enable or real paper state mutation.
- No paper admission or shadow launch actual execution.
- No paper-mode launch or production config patch.
- No Telegram real send.
- Board dossier is strictly metadata and not an activation approval.
- Acceptance board seal is metadata-only and does not grant permissions.
- Shadow-launch blocker denies real launches; it only records metadata attempts.
- Output metrics and decisions are NOT investment advice.
"""

def board_dossier_full_review_to_text(review: BoardDossierFullReview, limit: int = 100) -> str:
    lines = [f"Board Dossier Full Review ({review.review_id}):"]

    if review.dossiers:
        dossier = review.dossiers[0]
        lines.append(f"  Dossier Status: {dossier.status.name}")
        lines.append(f"  Decision: {dossier.decision.name}")

    lines.append(f"  Evidence: {len(review.evidence_items)} items")
    lines.append(f"  Seals: {len(review.acceptance_board_seals)}")
    lines.append(f"  Blocker Events: {len(review.shadow_launch_blocker_events)}")

    if review.shadow_launch_blocker_events:
        blocked = sum(1 for e in review.shadow_launch_blocker_events if e.blocked)
        lines.append(f"  Shadow Launch Attempts Blocked: {blocked}/{len(review.shadow_launch_blocker_events)}")

    lines.append(board_dossier_limitations_text())

    return "\n".join(lines)
