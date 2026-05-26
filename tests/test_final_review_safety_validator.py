import unittest
from usa_signal_bot.provider_freeze.final_review_safety_validator import validate_multi_provider_final_review_safety
from usa_signal_bot.provider_freeze.phase114_models import MultiProviderFinalReviewReport

class TestFinalReviewSafetyValidator(unittest.TestCase):
    def test_safety(self):
        report = MultiProviderFinalReviewReport(report_id="test", created_at_utc="test")
        # report initially has failures so boundary failed
        errors = validate_multi_provider_final_review_safety(report)
        self.assertGreater(len(errors), 0)
