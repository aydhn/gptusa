from typing import Any, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import FirewallAuditReview, create_firewall_audit_review_id
from usa_signal_bot.core.enums import FirewallAuditReportType

def build_firewall_audit_review(pre_rehearsal_payload: Optional[dict[str, Any]] = None, final_handoff_payload: Optional[dict[str, Any]] = None) -> FirewallAuditReview:
    return FirewallAuditReview(
        review_id=create_firewall_audit_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=FirewallAuditReportType.FULL_FIREWALL_AUDIT_REVIEW,
        replay_plans=[],
        replay_results=[],
        zero_mutation_audits=[],
        evidence_refreshes=[],
        readiness_checkpoints=[],
        audit_entries=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def firewall_audit_review_summary(review: FirewallAuditReview) -> dict[str, Any]:
    return {"id": review.review_id, "type": review.report_type.value}

def firewall_audit_limitations_text() -> str:
    return "LIMITATIONS: No broker/live/demo order. No active paper enable. No real paper mutation. No Telegram real send. No production config patch. Firewall replay is metadata-only. Zero-mutation audit is not activation. Evidence refresh is not activation. Not investment advice."

def firewall_audit_review_to_text(review: FirewallAuditReview, limit: int = 100) -> str:
    return f"Review {review.review_id} - {review.report_type.value}"
