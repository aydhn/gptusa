"""Test corporate action store."""
from usa_signal_bot.corporate_actions.corporate_action_store import write_corporate_action_review_result_json, list_corporate_action_reviews
from usa_signal_bot.corporate_actions.corporate_action_models import CorporateActionReviewResult
from usa_signal_bot.core.enums import CorporateActionReportType

def test_corporate_action_store(tmp_path):
    res = CorporateActionReviewResult("id", "2024", CorporateActionReportType.FULL_CORPORATE_ACTION_REVIEW, [], [])
    p = write_corporate_action_review_result_json(tmp_path / "corporate_actions" / "reviews" / "rev.json", res)
    assert p.exists()
    assert len(list_corporate_action_reviews(tmp_path)) == 1
