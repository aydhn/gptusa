from usa_signal_bot.release_packaging.compatibility_checker import check_bundle_schema_compatibility
from usa_signal_bot.release_packaging.packaging_models import BundleManifest

def test_compat():
    man = BundleManifest(
        manifest_id="1", created_at_utc="", bundle_id="1", bundle_version="1",
        bundle_type=None, bundle_status=None, source_candidate_id=None, source_experiment_id=None,
        source_governance_review_id=None, artifacts=[], required_artifact_types=[], missing_artifact_types=[],
        manifest_hash=None, schema_version="1.0", warnings=[], errors=[]
    )
    assert check_bundle_schema_compatibility(man).value == "COMPATIBLE"
