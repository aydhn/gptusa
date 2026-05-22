from typing import Any, Dict
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperDryRehearsalPlan,
    PrePaperDryRehearsalRun,
    ActivationDeniedCheckpoint,
    PrePaperDryRehearsalReview
)
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_plan import build_pre_paper_dry_rehearsal_plan
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_runner import GuardedPrePaperDryRehearsalRunner
from usa_signal_bot.paper_pre_rehearsal.activation_denied_checkpoint import build_activation_denied_checkpoint
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_report import build_pre_paper_dry_rehearsal_review

def pre_paper_plan_from_final_handoff(payload: Dict[str, Any]) -> PrePaperDryRehearsalPlan:
    return build_pre_paper_dry_rehearsal_plan(payload)

def pre_paper_run_from_final_handoff(payload: Dict[str, Any]) -> PrePaperDryRehearsalRun:
    plan = pre_paper_plan_from_final_handoff(payload)
    runner = GuardedPrePaperDryRehearsalRunner()
    return runner.run_rehearsal(plan)

def activation_checkpoint_from_final_handoff(payload: Dict[str, Any]) -> ActivationDeniedCheckpoint:
    run = pre_paper_run_from_final_handoff(payload)
    return build_activation_denied_checkpoint(run)

def pre_paper_review_from_final_handoff(payload: Dict[str, Any]) -> PrePaperDryRehearsalReview:
    run = pre_paper_run_from_final_handoff(payload)
    checkpoint = build_activation_denied_checkpoint(run)
    return build_pre_paper_dry_rehearsal_review(run, checkpoint)

def attach_pre_paper_metadata_to_final_handoff_payload(payload: Dict[str, Any], review: PrePaperDryRehearsalReview) -> Dict[str, Any]:
    updated = payload.copy()
    updated["guarded_pre_paper_rehearsal_review_id"] = review.review_id
    if review.activation_checkpoints:
        updated["activation_denied_checkpoint_id"] = review.activation_checkpoints[0].checkpoint_id
    return updated

def final_handoff_pre_paper_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "has_review": "guarded_pre_paper_rehearsal_review_id" in payload,
        "has_checkpoint": "activation_denied_checkpoint_id" in payload
    }

def final_handoff_adapter_to_text(payload: Dict[str, Any]) -> str:
    s = final_handoff_pre_paper_summary(payload)
    return f"Final Handoff Adapter: Attached Review={s['has_review']}, Attached Checkpoint={s['has_checkpoint']}"
