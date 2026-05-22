from typing import Any
import datetime

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReviewerNote,
    create_reviewer_note_id
)

def build_empty_reviewer_note(bundle_id: str | None = None, candidate_id: str | None = None) -> ReviewerNote:
    return ReviewerNote(
        note_id=create_reviewer_note_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        reviewer_id=None,
        candidate_id=candidate_id,
        bundle_id=bundle_id,
        note_text="",
        decision_hint=None,
        requires_followup=False,
        followups=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_reviewer_note(note_text: str, reviewer_id: str | None = None, bundle_id: str | None = None, candidate_id: str | None = None) -> ReviewerNote:
    note = build_empty_reviewer_note(bundle_id, candidate_id)
    note.note_text = note_text
    note.reviewer_id = reviewer_id

    errors = validate_reviewer_note_safety(note)
    if errors:
        note.errors.extend(errors)

    return note

def reviewer_note_requires_followup(note: ReviewerNote) -> bool:
    return note.requires_followup or len(note.followups) > 0

def validate_reviewer_note_safety(note: ReviewerNote) -> list[str]:
    errors = []
    text = note.note_text.lower()
    dangerous_keywords = [
        "aktif et", "canlıya al", "emir gönder", "live approved", "sent to broker",
        "kesin al", "garanti", "paper'a uygula", "gerçek emir", "kesin kâr", "candidate kesin iyi"
    ]
    for kw in dangerous_keywords:
        if kw in text:
             errors.append(f"Unsafe language detected in reviewer note: '{kw}'")
    return errors

def reviewer_note_summary(note: ReviewerNote) -> dict[str, Any]:
    return {
        "note_id": note.note_id,
        "reviewer_id": note.reviewer_id,
        "length": len(note.note_text),
        "has_errors": len(note.errors) > 0
    }

def reviewer_note_to_text(note: ReviewerNote) -> str:
    summary = reviewer_note_summary(note)
    return f"Reviewer Note: {summary['note_id']}, Errors: {summary['has_errors']}"
