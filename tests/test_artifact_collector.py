from usa_signal_bot.release_packaging.artifact_collector import required_bundle_artifact_types
from usa_signal_bot.core.enums import ReleaseBundleType

def test_collector():
    reqs = required_bundle_artifact_types(ReleaseBundleType.LOCAL_RESEARCH_CANDIDATE)
    assert len(reqs) > 0
