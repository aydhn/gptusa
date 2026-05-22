from usa_signal_bot.paper_readiness_confirmation.confirmation_report import build_readiness_confirmation_review, readiness_confirmation_review_summary
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle

def test_build_readiness_confirmation_review():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    review = build_readiness_confirmation_review(q, b)

    assert len(review.queue_items) == 1
    assert len(review.bundles) == 1

    summary = readiness_confirmation_review_summary(review)
    assert "No broker/live/demo order" in summary["limitations"]
