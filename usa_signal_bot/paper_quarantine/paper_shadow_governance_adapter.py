import datetime
from typing import Any

from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    SupervisedDryRunBridgePlan,
    QuarantineEnrollmentReview,
    create_quarantined_candidate_id,
)
from usa_signal_bot.paper_quarantine.eligibility_checker import (
    evaluate_quarantine_eligibility,
    candidate_status_from_enrollment_decision,
    quarantine_safety_flags_from_shadow_governance
)
from usa_signal_bot.paper_quarantine.shadow_governance_ingestion import (
    extract_shadow_acceptance_score,
)
from usa_signal_bot.paper_quarantine.quarantine_policy import default_quarantine_policy
from usa_signal_bot.paper_quarantine.paper_snapshot_ref import build_read_only_paper_snapshot_ref
from usa_signal_bot.paper_quarantine.promotion_ticket import build_promotion_ticket_for_candidate
from usa_signal_bot.paper_quarantine.bridge_planner import build_supervised_dry_run_bridge_plan
from usa_signal_bot.paper_quarantine.enrollment_report import build_quarantine_enrollment_review

def candidate_from_shadow_governance_review(payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None) -> QuarantinedPaperCandidate:
    decision = evaluate_quarantine_eligibility(payload)
    status = candidate_status_from_enrollment_decision(decision)
    flags = quarantine_safety_flags_from_shadow_governance(payload)
    score = extract_shadow_acceptance_score(payload)
    policy = default_quarantine_policy()
    snapshot_ref = build_read_only_paper_snapshot_ref(paper_snapshot) if paper_snapshot else None

    return QuarantinedPaperCandidate(
        candidate_id=create_quarantined_candidate_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=status,
        source_bundle_id=payload.get("bundle_id"),
        source_bundle_version=payload.get("bundle_version"),
        source_shadow_governance_review_id=payload.get("review_id"),
        source_shadow_decision=payload.get("decision"),
        shadow_acceptance_score=score,
        risk_flags=flags,
        policy=policy,
        paper_snapshot_ref=snapshot_ref,
        promotion_ticket_id=None,
        bridge_plan_id=None,
        review_due_at_utc=None,
        allowed_for_active_paper=False,
        allowed_for_broker_execution=False,
        warnings=[],
        errors=[]
    )

def ticket_from_shadow_governance_review(payload: dict[str, Any]) -> ReadOnlyPromotionTicket:
    candidate = candidate_from_shadow_governance_review(payload)
    decision = evaluate_quarantine_eligibility(payload)
    ticket = build_promotion_ticket_for_candidate(candidate, decision, evidence_refs=[payload.get("review_id", "")])
    return ticket

def bridge_plan_from_shadow_governance_review(payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None) -> SupervisedDryRunBridgePlan:
    candidate = candidate_from_shadow_governance_review(payload, paper_snapshot)
    decision = evaluate_quarantine_eligibility(payload)
    ticket = build_promotion_ticket_for_candidate(candidate, decision)
    return build_supervised_dry_run_bridge_plan(candidate, ticket, candidate.policy)

def quarantine_review_from_shadow_governance_review(payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None) -> QuarantineEnrollmentReview:
    candidate = candidate_from_shadow_governance_review(payload, paper_snapshot)
    decision = evaluate_quarantine_eligibility(payload)
    ticket = build_promotion_ticket_for_candidate(candidate, decision)
    bridge_plan = build_supervised_dry_run_bridge_plan(candidate, ticket, candidate.policy)

    candidate.promotion_ticket_id = ticket.ticket_id
    candidate.bridge_plan_id = bridge_plan.bridge_plan_id

    return build_quarantine_enrollment_review(candidate, ticket, bridge_plan)

def attach_quarantine_to_shadow_governance_payload(payload: dict[str, Any], review: QuarantineEnrollmentReview) -> dict[str, Any]:
    payload["quarantine_review_id"] = review.review_id
    payload["quarantine_status"] = review.candidates[0].status.value if review.candidates else "unknown"
    return payload

def paper_shadow_governance_adapter_to_text(payload: dict[str, Any]) -> str:
    review_id = payload.get("quarantine_review_id", "unknown")
    status = payload.get("quarantine_status", "unknown")
    return f"Shadow Governance Quarantine Adapter\nReview ID: {review_id}\nStatus: {status}"
