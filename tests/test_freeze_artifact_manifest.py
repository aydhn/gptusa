import unittest
from usa_signal_bot.provider_freeze.freeze_bundle_builder import build_provider_expansion_freeze_bundle
from usa_signal_bot.provider_freeze.freeze_evidence_collector import collect_provider_freeze_evidence
from usa_signal_bot.provider_freeze.freeze_artifact_manifest import build_provider_freeze_artifact_manifest, validate_provider_freeze_artifact_manifest

class TestFreezeArtifactManifest(unittest.TestCase):
    def test_manifest(self):
        items = collect_provider_freeze_evidence()
        bundle = build_provider_expansion_freeze_bundle(items)
        manifest = build_provider_freeze_artifact_manifest(bundle)
        errors = validate_provider_freeze_artifact_manifest(manifest)
        self.assertEqual(len(errors), 0)
