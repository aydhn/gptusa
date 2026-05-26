import sys
import unittest
sys.path.insert(0, '.')

from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderGovernanceIngestionResult,
    ProviderFreezeEvidenceItem,
    ProviderExpansionFreezeBundle,
    MultiProviderReviewItem,
    MultiProviderFinalReviewReport,
    DataLayerRehearsalScenario,
    DataLayerRehearsalStep,
    DataLayerRehearsalReport,
    DataLayerOutputContract,
    ProviderFreezeArtifactManifest,
    ProviderFreezeContext,
    ProviderFreezeFullReview
)
from usa_signal_bot.provider_freeze.freeze_bundle_builder import build_provider_expansion_freeze_bundle
from usa_signal_bot.provider_freeze.freeze_evidence_collector import freeze_evidence_item_from_payload
from usa_signal_bot.provider_freeze.multi_provider_review import build_multi_provider_final_review_report
from usa_signal_bot.provider_freeze.rehearsal_runner import DataLayerRehearsalRunner

class TestPhase114(unittest.TestCase):
    def test_models_exist(self):
        self.assertIsNotNone(ProviderGovernanceIngestionResult)
        self.assertIsNotNone(ProviderFreezeEvidenceItem)
        self.assertIsNotNone(ProviderExpansionFreezeBundle)

    def test_freeze_bundle_builder(self):
        item = freeze_evidence_item_from_payload(106, "phase106_provider_abstraction", {"test": "data"})
        bundle = build_provider_expansion_freeze_bundle([item])
        self.assertTrue(bundle.frozen)
        self.assertTrue(bundle.immutable)
        self.assertEqual(bundle.phase_start, 106)
        self.assertEqual(bundle.phase_end, 114)

    def test_multi_provider_review(self):
        report = build_multi_provider_final_review_report([])
        self.assertGreater(report.total_items, 0)
        self.assertFalse(report.multi_provider_review_passed)

    def test_rehearsal_runner(self):
        runner = DataLayerRehearsalRunner()
        report = runner.run()
        self.assertTrue(report.rehearsal_passed)

if __name__ == '__main__':
    unittest.main()
