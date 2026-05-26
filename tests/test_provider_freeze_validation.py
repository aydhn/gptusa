import unittest
from usa_signal_bot.provider_freeze.provider_freeze_validation import validate_no_execution_language_in_freeze_text

class TestProviderFreezeValidation(unittest.TestCase):
    def test_bad_text(self):
        report = validate_no_execution_language_in_freeze_text("this has a buy signal")
        self.assertFalse(report.valid)
