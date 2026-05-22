from usa_signal_bot.paper_readiness_confirmation.human_review_summary import build_human_review_summary
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item

def test_build_human_review_summary():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    summary = build_human_review_summary(b)

    assert summary["bundle_id"] == b.bundle_id
    assert summary["risk_summary"]["activation_allowed"] is False
