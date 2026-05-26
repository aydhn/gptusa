import unittest
from pathlib import Path
from usa_signal_bot.provider_freeze.provider_freeze_store import provider_freeze_store_summary

class TestProviderFreezeStore(unittest.TestCase):
    def test_summary(self):
        summary = provider_freeze_store_summary(Path("data"))
        self.assertIn("contexts", summary)
