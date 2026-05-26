import unittest
from usa_signal_bot.provider_freeze.provider_safety_final_checker import check_no_execution_boundary

class TestSafetyFinalChecker(unittest.TestCase):
    def test_no_execution_boundary_missing(self):
        item = check_no_execution_boundary([])
        self.assertFalse(item.passed)
