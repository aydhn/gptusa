from typing import Any, Dict
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    ReadinessRehearsalRun, FinalReviewLock, GuardedHandoffRegistryEntry, ReadinessRehearsalReview
)
from usa_signal_bot.paper_readiness_rehearsal.stage_rehearsal_planner import build_default_stage_rehearsal_plans
from usa_signal_bot.paper_readiness_rehearsal.stage_rehearsal_runner import StagedReadinessRehearsalRunner
from usa_signal_bot.paper_readiness_rehearsal.final_review_lock import build_final_review_lock
from usa_signal_bot.paper_readiness_rehearsal.handoff_evidence_index import build_handoff_evidence_index
from usa_signal_bot.paper_readiness_rehearsal.handoff_registry import build_guarded_handoff_registry_entry
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_report import build_readiness_rehearsal_review

def readiness_rehearsal_from_promotion_dossier_review(payload: Dict[str, Any]) -> ReadinessRehearsalRun:
    plans = build_default_stage_rehearsal_plans()
    runner = StagedReadinessRehearsalRunner()
    return runner.run_rehearsal(plans)

def final_lock_from_promotion_dossier_review(payload: Dict[str, Any]) -> FinalReviewLock:
    run = readiness_rehearsal_from_promotion_dossier_review(payload)
    return build_final_review_lock(run, payload)

def handoff_entry_from_promotion_dossier_review(payload: Dict[str, Any]) -> GuardedHandoffRegistryEntry:
    run = readiness_rehearsal_from_promotion_dossier_review(payload)
    lock = final_lock_from_promotion_dossier_review(payload)
    evidence_index = build_handoff_evidence_index(payload, run, lock)
    return build_guarded_handoff_registry_entry(run, lock, evidence_index)

def readiness_rehearsal_review_from_promotion_dossier_review(payload: Dict[str, Any]) -> ReadinessRehearsalReview:
    run = readiness_rehearsal_from_promotion_dossier_review(payload)
    lock = build_final_review_lock(run, payload)
    evidence_index = build_handoff_evidence_index(payload, run, lock)
    handoff_entry = build_guarded_handoff_registry_entry(run, lock, evidence_index)
    return build_readiness_rehearsal_review(run, lock, handoff_entry, evidence_index)

def attach_readiness_rehearsal_metadata_to_promotion_payload(payload: Dict[str, Any], review: ReadinessRehearsalReview) -> Dict[str, Any]:
    new_payload = payload.copy()
    new_payload["readiness_rehearsal_metadata"] = {
        "review_id": review.review_id,
        "runs_count": len(review.rehearsal_runs)
    }
    return new_payload

def promotion_dossier_readiness_rehearsal_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    meta = payload.get("readiness_rehearsal_metadata", {})
    return {"has_rehearsal": bool(meta), "review_id": meta.get("review_id")}

def promotion_dossier_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = promotion_dossier_readiness_rehearsal_summary(payload)
    return f"Promotion Dossier Adapter: Has Rehearsal={summary['has_rehearsal']}"
