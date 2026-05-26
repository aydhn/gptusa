import unittest
from usa_signal_bot.provider_freeze.provider_coverage_checker import check_provider_coverage

class TestCoverageChecker(unittest.TestCase):
    def test_coverage_missing(self):
        item = check_provider_coverage([])
        self.assertFalse(item.passed)
