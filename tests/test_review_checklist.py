from usa_signal_bot.paper_readiness_confirmation.review_checklist import (
    build_human_review_checklist_items,
    checklist_summary
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item
from usa_signal_bot.core.enums import ReviewChecklistItemStatus

def test_build_human_review_checklist_items():
    q = build_default_confirmation_queue_item()
    items = build_human_review_checklist_items(q)
    assert len(items) == 7
    for item in items:
        assert item.status == ReviewChecklistItemStatus.NOT_REVIEWED
        assert item.required is True

def test_checklist_summary():
    q = build_default_confirmation_queue_item()
    items = build_human_review_checklist_items(q)
    summary = checklist_summary(items)
    assert summary[ReviewChecklistItemStatus.NOT_REVIEWED.value] == 7
