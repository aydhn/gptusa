import unittest
from usa_signal_bot.provider_freeze.provider_freeze_report import build_provider_freeze_full_review

class TestProviderFreezeReport(unittest.TestCase):
    def test_review(self):
        review = build_provider_freeze_full_review()
        self.assertIsNotNone(review.review_id)
