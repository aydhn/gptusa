import unittest
from usa_signal_bot.provider_freeze.provider_consistency_checker import check_provider_registry_consistency

class TestConsistencyChecker(unittest.TestCase):
    def test_registry_consistency_missing(self):
        item = check_provider_registry_consistency([])
        self.assertFalse(item.passed)
