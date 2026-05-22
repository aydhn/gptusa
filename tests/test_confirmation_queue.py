from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import (
    build_default_confirmation_queue_item,
    build_readiness_confirmation_queue_item,
    validate_confirmation_queue_item_safety
)
from usa_signal_bot.core.enums import ReadinessConfirmationQueueStatus

def test_build_default_confirmation_queue_item():
    item = build_default_confirmation_queue_item()
    assert item.status == ReadinessConfirmationQueueStatus.DRAFT
    assert item.manual_review_required is True
    assert item.activation_denied_required is True
    assert item.allows_active_paper is False

def test_validate_confirmation_queue_item_safety():
    item = build_default_confirmation_queue_item()
    errors = validate_confirmation_queue_item_safety(item)
    assert len(errors) == 0

    item.allows_active_paper = True
    errors = validate_confirmation_queue_item_safety(item)
    assert len(errors) == 1
    assert "allows_active_paper must be False" in errors[0]

def test_build_readiness_confirmation_queue_item():
    payload = {
        "decision": "CONTINUE_WITH_ACTIVATION_DENIED_AUDIT",
        "activation_allowed": False,
        "zero_mutation_audit": {"status": "PASSED"}
    }
    item = build_readiness_confirmation_queue_item(payload)
    assert item.status == ReadinessConfirmationQueueStatus.QUEUED
