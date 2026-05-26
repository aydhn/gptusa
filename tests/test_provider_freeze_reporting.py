import unittest
from usa_signal_bot.provider_freeze.provider_freeze_reporting import provider_freeze_limitations_text

class TestProviderFreezeReporting(unittest.TestCase):
    def test_text(self):
        text = provider_freeze_limitations_text()
        self.assertIn("Phase 114 Limitations", text)
