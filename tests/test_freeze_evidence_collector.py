import unittest
from usa_signal_bot.provider_freeze.freeze_evidence_collector import required_freeze_evidence_names, collect_provider_freeze_evidence

class TestFreezeEvidenceCollector(unittest.TestCase):
    def test_required_names(self):
        names = required_freeze_evidence_names()
        self.assertIn("phase106_provider_abstraction", names)

    def test_collect(self):
        items = collect_provider_freeze_evidence()
        self.assertGreater(len(items), 0)
