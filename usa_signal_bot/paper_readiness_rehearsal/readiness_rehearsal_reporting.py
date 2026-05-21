from typing import Any, Dict
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    StageRehearsalPlan, StageRehearsalResult, ReadinessRehearsalRun,
    FinalReviewLock, GuardedHandoffRegistryEntry, HandoffEvidenceIndex,
    ReadinessRehearsalAuditEntry, ReadinessRehearsalReview
)
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_report import readiness_rehearsal_limitations_text

def stage_rehearsal_plan_to_text(item: StageRehearsalPlan) -> str:
    return f"Stage Plan {item.stage_plan_id}: {item.stage_title} [{item.source_stage}] -> {item.status.value}"

def stage_rehearsal_result_to_text(item: StageRehearsalResult) -> str:
    return f"Stage Result {item.result_id}: [{item.source_stage}] -> {item.status.value}"

def readiness_rehearsal_run_to_text(item: ReadinessRehearsalRun, limit: int = 100) -> str:
    lines = [f"Rehearsal Run {item.run_id} ({item.status.value}):"]
    lines.append(f"Decision: {item.decision.value}")
    lines.append(f"Safety Flags: {[f.value for f in item.safety_flags]}")
    for p in item.stage_plans[:limit]:
        lines.append("  " + stage_rehearsal_plan_to_text(p))
    return "\n".join(lines)

def final_review_lock_to_text(item: FinalReviewLock) -> str:
    return f"Final Lock {item.lock_id} ({item.status.value}): Locked={item.locked} Hash={item.lock_hash}"

def guarded_handoff_registry_entry_to_text(item: GuardedHandoffRegistryEntry) -> str:
    return f"Handoff Entry {item.handoff_id} ({item.status.value}): Decision={item.decision.value}"

def handoff_evidence_index_to_text(item: HandoffEvidenceIndex) -> str:
    return f"Evidence Index {item.evidence_index_id}: Score={item.evidence_score} Missing={len(item.missing_evidence_types)}"

def readiness_rehearsal_audit_entry_to_text(item: ReadinessRehearsalAuditEntry) -> str:
    return f"Audit [{item.created_at_utc}] {item.action} on {item.entity_id}: {item.decision}"

def readiness_rehearsal_review_to_text(item: ReadinessRehearsalReview, limit: int = 100) -> str:
    lines = [f"Full Review {item.review_id}:"]
    lines.append(f"Runs: {len(item.rehearsal_runs)}")
    lines.append(f"Locks: {len(item.final_locks)}")
    lines.append(f"Handoffs: {len(item.handoff_entries)}")
    lines.append(readiness_rehearsal_limitations_text())
    return "\n".join(lines)

def readiness_rehearsal_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in summary.items()])
