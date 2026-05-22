from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import (
    build_human_review_bundle,
    validate_human_review_bundle_safety
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item
from usa_signal_bot.core.enums import HumanReviewBundleStatus

def test_build_human_review_bundle():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    assert b.status == HumanReviewBundleStatus.CREATED
    assert b.activation_denied is True
    assert b.activation_allowed is False
    assert b.allows_active_paper is False

def test_validate_human_review_bundle_safety():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    errors = validate_human_review_bundle_safety(b)
    assert len(errors) == 0

    b.activation_allowed = True
    errors = validate_human_review_bundle_safety(b)
    assert len(errors) == 1
    assert "activation_allowed must be False" in errors[0]
