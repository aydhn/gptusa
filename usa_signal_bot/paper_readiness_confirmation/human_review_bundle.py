from typing import Any
import datetime

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    HumanReviewBundle,
    ReadinessConfirmationQueueItem,
    HumanReviewChecklistItem,
    ReviewerNote,
    create_human_review_bundle_id
)
from usa_signal_bot.core.enums import HumanReviewBundleStatus
from usa_signal_bot.paper_readiness_confirmation.review_checklist import checklist_summary
from usa_signal_bot.paper_readiness_confirmation.reviewer_notes import reviewer_note_summary

def build_human_review_bundle(
    queue_item: ReadinessConfirmationQueueItem,
    checklist_items: list[HumanReviewChecklistItem] | None = None,
    reviewer_notes: list[ReviewerNote] | None = None
) -> HumanReviewBundle:

    c_items = checklist_items or []
    notes = reviewer_notes or []

    bundle = HumanReviewBundle(
        bundle_id=create_human_review_bundle_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=HumanReviewBundleStatus.CREATED,
        candidate_id=queue_item.candidate_id,
        queue_item_id=queue_item.queue_item_id,
        title=f"Human Review Bundle for {queue_item.candidate_id or 'Unknown'}",
        summary={},
        checklist_refs=[c.checklist_item_id for c in c_items],
        evidence_refs=list(queue_item.evidence_refs),
        reviewer_note_refs=[n.note_id for n in notes],
        required_reviewer_actions=[],
        safety_flags=list(queue_item.safety_flags),
        activation_denied=True,
        activation_allowed=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        warnings=[],
        errors=[],
        metadata={}
    )

    bundle.summary = {
        "checklist": checklist_summary(c_items),
        "notes_count": len(notes)
    }

    return bundle

def human_review_bundle_summary(bundle: HumanReviewBundle) -> dict[str, Any]:
    return {
        "bundle_id": bundle.bundle_id,
        "status": bundle.status.value,
        "candidate_id": bundle.candidate_id,
        "checklists": len(bundle.checklist_refs),
        "notes": len(bundle.reviewer_note_refs)
    }

def validate_human_review_bundle_safety(bundle: HumanReviewBundle) -> list[str]:
    errors = []
    if not bundle.activation_denied:
         errors.append("activation_denied must be True")
    if bundle.activation_allowed:
         errors.append("activation_allowed must be False")
    if bundle.allows_active_paper:
         errors.append("allows_active_paper must be False")
    if bundle.allows_broker_execution:
         errors.append("allows_broker_execution must be False")
    if bundle.allows_paper_state_mutation:
         errors.append("allows_paper_state_mutation must be False")
    if bundle.allows_config_patch:
         errors.append("allows_config_patch must be False")
    if bundle.allows_telegram_real_send:
         errors.append("allows_telegram_real_send must be False")
    return errors

def human_review_bundle_required_actions(bundle: HumanReviewBundle) -> list[str]:
    return bundle.required_reviewer_actions

def human_review_bundle_to_text(bundle: HumanReviewBundle, limit: int = 100) -> str:
    summary = human_review_bundle_summary(bundle)
    return f"Bundle: {summary['bundle_id']}, Status: {summary['status']}"
