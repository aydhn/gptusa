from typing import Any, List
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import *

def firewall_replay_plan_to_text(item: FirewallReplayPlan) -> str: return f"Plan {item.replay_plan_id}"
def firewall_replay_result_to_text(item: FirewallReplayResult) -> str: return f"Result {item.replay_result_id}"
def zero_mutation_baseline_to_text(item: ZeroMutationBaseline) -> str: return f"Baseline {item.baseline_id}"
def zero_mutation_audit_report_to_text(item: ZeroMutationAuditReport) -> str: return f"Audit {item.audit_id}"
def pre_paper_readiness_evidence_item_to_text(item: PrePaperReadinessEvidenceItem) -> str: return f"Evidence {item.evidence_id}"
def pre_paper_readiness_evidence_refresh_to_text(item: PrePaperReadinessEvidenceRefresh, limit: int = 100) -> str: return f"Refresh {item.refresh_id}"
def readiness_audit_checkpoint_to_text(item: ReadinessAuditCheckpoint) -> str: return f"Checkpoint {item.checkpoint_id}"
def firewall_audit_trail_entry_to_text(item: FirewallAuditTrailEntry) -> str: return f"TrailEntry {item.audit_entry_id}"
def firewall_audit_review_to_text(item: FirewallAuditReview, limit: int = 100) -> str: return f"Review {item.review_id}"

def firewall_audit_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary.get('reviews', 0)} reviews"

def firewall_audit_limitations_text() -> str:
    return "No broker/live/demo order. No active paper enable. No real paper mutation. No Telegram real send. No production config patch. Firewall replay is metadata-only. Zero-mutation audit is not activation. Evidence refresh is not activation. Not investment advice."
