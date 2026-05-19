from usa_signal_bot.release_packaging.manifest_builder import build_bundle_manifest
from usa_signal_bot.core.enums import ReleaseBundleType

def test_manifest():
    man = build_bundle_manifest("bundle_1", "0.1.0", ReleaseBundleType.LOCAL_RESEARCH_CANDIDATE, [])
    assert len(man.missing_artifact_types) > 0
