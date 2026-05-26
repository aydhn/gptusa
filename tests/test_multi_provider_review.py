import unittest
from usa_signal_bot.provider_freeze.multi_provider_review import build_multi_provider_final_review_report

class TestMultiProviderReview(unittest.TestCase):
    def test_review(self):
        report = build_multi_provider_final_review_report([])
        self.assertGreater(report.total_items, 0)
