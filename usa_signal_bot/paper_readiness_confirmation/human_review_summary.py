from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    HumanReviewBundle,
    HumanReviewChecklistItem,
    ReviewerNote
)
from usa_signal_bot.paper_readiness_confirmation.review_checklist import checklist_summary
from usa_signal_bot.paper_readiness_confirmation.reviewer_notes import reviewer_note_requires_followup

def build_human_review_summary(
    bundle: HumanReviewBundle,
    checklist_items: list[HumanReviewChecklistItem] | None = None,
    reviewer_notes: list[ReviewerNote] | None = None
) -> dict[str, Any]:
    c_items = checklist_items or []
    notes = reviewer_notes or []

    return {
        "bundle_id": bundle.bundle_id,
        "candidate_id": bundle.candidate_id,
        "checklist_summary": summarize_checklist_statuses(c_items),
        "notes_summary": summarize_reviewer_notes(notes),
        "risk_summary": human_review_bundle_risk_summary(bundle)
    }

def summarize_checklist_statuses(items: list[HumanReviewChecklistItem]) -> dict[str, int]:
    return checklist_summary(items)

def summarize_reviewer_notes(notes: list[ReviewerNote]) -> dict[str, Any]:
    return {
        "total_notes": len(notes),
        "require_followup": sum(1 for n in notes if reviewer_note_requires_followup(n))
    }

def human_review_bundle_risk_summary(bundle: HumanReviewBundle) -> dict[str, Any]:
    return {
        "activation_allowed": bundle.activation_allowed,
        "flags": [f.value for f in bundle.safety_flags]
    }

def human_review_summary_to_text(payload: dict[str, Any]) -> str:
    return f"Review Summary for {payload.get('bundle_id')}"
