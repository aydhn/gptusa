import datetime
from typing import Any

from usa_signal_bot.core.enums import PromotionTicketStatus, QuarantineSafetyFlag
from usa_signal_bot.paper_quarantine.quarantine_models import (
    ReadOnlyPromotionTicket,
    QuarantinedPaperCandidate,
    create_promotion_ticket_id,
    validate_read_only_promotion_ticket,
)
from usa_signal_bot.paper_quarantine.eligibility_checker import (
    evaluate_quarantine_eligibility,
    quarantine_safety_flags_from_shadow_governance
)
from usa_signal_bot.paper_quarantine.shadow_governance_ingestion import (
    extract_shadow_acceptance_score,
    extract_shadow_required_followups
)

def build_promotion_ticket_for_candidate(
    candidate: QuarantinedPaperCandidate,
    decision: 'QuarantineEnrollmentDecision',
    evidence_refs: list[str] | None = None
) -> ReadOnlyPromotionTicket:

    ticket = ReadOnlyPromotionTicket(
        ticket_id=create_promotion_ticket_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=PromotionTicketStatus.READ_ONLY_CREATED,
        candidate_id=candidate.candidate_id,
        source_bundle_id=candidate.source_bundle_id,
        source_bundle_version=candidate.source_bundle_version,
        source_shadow_governance_review_id=candidate.source_shadow_governance_review_id,
        enrollment_decision=decision,
        title=f"Quarantine Promotion for {candidate.source_bundle_id or 'Unknown'}",
        description="Read-only promotion ticket generated for quarantined candidate enrollment.",
        evidence_refs=evidence_refs or [],
        acceptance_score=candidate.shadow_acceptance_score,
        risk_flags=candidate.risk_flags.copy(),
        required_followups=[],
        manual_review_required=True,
        manual_review_completed=False,
        read_only=True,
        allowed_for_active_paper=False,
        allowed_for_config_patch=False,
        allowed_for_broker_execution=False,
        warnings=[],
        errors=[]
    )
    validate_read_only_promotion_ticket(ticket)
    return ticket

def build_ticket_from_shadow_governance_payload(payload: dict[str, Any]) -> ReadOnlyPromotionTicket:
    decision = evaluate_quarantine_eligibility(payload)
    score = extract_shadow_acceptance_score(payload)
    flags = quarantine_safety_flags_from_shadow_governance(payload)
    followups = extract_shadow_required_followups(payload)

    ticket = ReadOnlyPromotionTicket(
        ticket_id=create_promotion_ticket_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=PromotionTicketStatus.READ_ONLY_CREATED,
        candidate_id=None,
        source_bundle_id=payload.get("bundle_id"),
        source_bundle_version=payload.get("bundle_version"),
        source_shadow_governance_review_id=payload.get("review_id"),
        enrollment_decision=decision,
        title=f"Shadow Governance Promotion for {payload.get('bundle_id', 'Unknown')}",
        description="Generated directly from shadow governance payload.",
        evidence_refs=[],
        acceptance_score=score,
        risk_flags=flags,
        required_followups=followups,
        manual_review_required=True,
        manual_review_completed=False,
        read_only=True,
        allowed_for_active_paper=False,
        allowed_for_config_patch=False,
        allowed_for_broker_execution=False,
        warnings=[],
        errors=[]
    )
    validate_read_only_promotion_ticket(ticket)
    return ticket

def promotion_ticket_summary(ticket: ReadOnlyPromotionTicket) -> dict[str, Any]:
    return {
        "ticket_id": ticket.ticket_id,
        "status": ticket.status.value,
        "enrollment_decision": ticket.enrollment_decision.value,
        "read_only": ticket.read_only,
        "allowed_for_active_paper": ticket.allowed_for_active_paper,
    }

def promotion_ticket_to_text(ticket: ReadOnlyPromotionTicket) -> str:
    lines = [
        f"Promotion Ticket: {ticket.ticket_id}",
        f"Status: {ticket.status.value}",
        f"Candidate ID: {ticket.candidate_id}",
        f"Decision: {ticket.enrollment_decision.value}",
        f"Score: {ticket.acceptance_score}",
        f"Read Only: {ticket.read_only}",
        f"Active Paper Allowed: {ticket.allowed_for_active_paper}",
    ]
    return "\n".join(lines)
