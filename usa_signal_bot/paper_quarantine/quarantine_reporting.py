from typing import Any
import json

from usa_signal_bot.paper_quarantine.quarantine_models import (
    QuarantinePolicy,
    PaperSnapshotRef,
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    SupervisedDryRunBridgePlan,
    QuarantineAuditEntry,
    QuarantineEnrollmentReview,
)
from usa_signal_bot.paper_quarantine.enrollment_report import quarantine_limitations_text

def quarantine_policy_to_text(item: QuarantinePolicy) -> str:
    from usa_signal_bot.paper_quarantine.quarantine_policy import quarantine_policy_to_text as q_text
    return q_text(item)

def paper_snapshot_ref_to_text(item: PaperSnapshotRef) -> str:
    from usa_signal_bot.paper_quarantine.paper_snapshot_ref import paper_snapshot_ref_to_text as s_text
    return s_text(item)

def quarantined_candidate_to_text(item: QuarantinedPaperCandidate) -> str:
    lines = [
        f"Quarantined Candidate: {item.candidate_id}",
        f"Status: {item.status.value}",
        f"Source Bundle: {item.source_bundle_id} (v{item.source_bundle_version})",
        f"Shadow Score: {item.shadow_acceptance_score}",
        f"Risk Flags: {[f.value for f in item.risk_flags]}",
        f"Review Due: {item.review_due_at_utc}",
        f"Ticket ID: {item.promotion_ticket_id}",
        f"Bridge Plan ID: {item.bridge_plan_id}",
        quarantine_limitations_text()
    ]
    return "\n".join(lines)

def promotion_ticket_to_text(item: ReadOnlyPromotionTicket) -> str:
    from usa_signal_bot.paper_quarantine.promotion_ticket import promotion_ticket_to_text as p_text
    return p_text(item) + "\n" + quarantine_limitations_text()

def bridge_plan_to_text(item: SupervisedDryRunBridgePlan) -> str:
    from usa_signal_bot.paper_quarantine.bridge_planner import bridge_plan_to_text as b_text
    return b_text(item) + "\n" + quarantine_limitations_text()

def quarantine_audit_entry_to_text(item: QuarantineAuditEntry) -> str:
    lines = [
        f"Audit Entry: {item.audit_id}",
        f"Action: {item.action}",
        f"Decision: {item.decision}",
        f"Rationale: {item.rationale}"
    ]
    return "\n".join(lines)

def quarantine_enrollment_review_to_text(item: QuarantineEnrollmentReview, limit: int = 100) -> str:
    from usa_signal_bot.paper_quarantine.enrollment_report import quarantine_enrollment_review_to_text as q_rev_text
    return q_rev_text(item, limit)

def quarantine_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = ["Quarantine Store Summary"]
    for k, v in summary.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)
