import unittest
from usa_signal_bot.provider_freeze.freeze_evidence_collector import collect_provider_freeze_evidence
from usa_signal_bot.provider_freeze.freeze_bundle_builder import build_provider_expansion_freeze_bundle

class TestFreezeBundleBuilder(unittest.TestCase):
    def test_build(self):
        # By default simulated empty items fail missing check
        items = collect_provider_freeze_evidence()
        bundle = build_provider_expansion_freeze_bundle(items)
        self.assertTrue(bundle.frozen)
