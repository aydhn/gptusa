from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import (
    PrePaperReadinessEvidenceItem, FirewallReplayResult, ZeroMutationAuditReport,
    create_pre_paper_evidence_item_id
)
from usa_signal_bot.core.enums import ReadinessEvidenceRefreshStatus

def required_pre_paper_readiness_evidence_types() -> List[str]:
    return [
        "final_handoff_full_review",
        "sealed_readiness_archive",
        "pre_paper_governance_checkpoint",
        "pre_paper_rehearsal_review",
        "pre_paper_dry_rehearsal_run",
        "mutation_firewall_rules",
        "mutation_firewall_events",
        "firewall_replay_result",
        "zero_mutation_audit",
        "activation_denied_checkpoint",
        "paper_baseline_before",
        "paper_baseline_after"
    ]

def collect_pre_paper_readiness_evidence(
    pre_rehearsal_payload: Optional[dict[str, Any]] = None,
    final_handoff_payload: Optional[dict[str, Any]] = None,
    firewall_replay_result: Optional[FirewallReplayResult] = None,
    zero_mutation_audit: Optional[ZeroMutationAuditReport] = None
) -> List[PrePaperReadinessEvidenceItem]:
    items = []

    # Pre-rehearsal evidence
    if pre_rehearsal_payload:
        items.append(evidence_item_from_source("pre_paper_rehearsal_review", pre_rehearsal_payload, pre_rehearsal_payload.get("review_id")))
        items.append(evidence_item_from_source("mutation_firewall_events", pre_rehearsal_payload.get("firewall_events")))
        items.append(evidence_item_from_source("activation_denied_checkpoint", pre_rehearsal_payload.get("activation_denied_checkpoint")))

    # Replay evidence
    if firewall_replay_result:
        items.append(evidence_item_from_source("firewall_replay_result", firewall_replay_result, firewall_replay_result.replay_result_id))

    # Zero mutation evidence
    if zero_mutation_audit:
        items.append(evidence_item_from_source("zero_mutation_audit", zero_mutation_audit, zero_mutation_audit.audit_id))
        items.append(evidence_item_from_source("paper_baseline_before", zero_mutation_audit.before_baseline))
        items.append(evidence_item_from_source("paper_baseline_after", zero_mutation_audit.after_baseline))

    return items

def evidence_item_from_source(evidence_type: str, source: Any, source_ref_id: Optional[str] = None, source_path: Optional[str] = None) -> PrePaperReadinessEvidenceItem:
    available = source is not None
    return PrePaperReadinessEvidenceItem(
        evidence_id=create_pre_paper_evidence_item_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        evidence_type=evidence_type,
        source_ref_id=source_ref_id,
        source_path=source_path,
        status=ReadinessEvidenceRefreshStatus.FRESH if available else ReadinessEvidenceRefreshStatus.MISSING,
        required=evidence_type in required_pre_paper_readiness_evidence_types(),
        available=available,
        fresh=available,
        stale=False,
        summary={},
        warnings=[],
        errors=[],
        metadata={}
    )

def evidence_collection_summary(items: List[PrePaperReadinessEvidenceItem]) -> dict[str, Any]:
    return {"total": len(items), "available": sum(1 for i in items if i.available)}

def evidence_refresh_collector_to_text(items: List[PrePaperReadinessEvidenceItem], limit: int = 100) -> str:
    return f"Collected {len(items)} evidence items"
