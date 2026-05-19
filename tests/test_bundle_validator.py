from usa_signal_bot.release_packaging.bundle_validator import validate_bundle_manifest_safety
from usa_signal_bot.release_packaging.packaging_models import BundleManifest

def test_validator():
    man = BundleManifest(
        manifest_id="1", created_at_utc="", bundle_id="1", bundle_version="1",
        bundle_type=None, bundle_status=None, source_candidate_id=None, source_experiment_id=None,
        source_governance_review_id=None, artifacts=[], required_artifact_types=[], missing_artifact_types=[],
        manifest_hash=None, schema_version="1.0", warnings=[], errors=[]
    )
    res = validate_bundle_manifest_safety(man)
    assert res.status.value == "PASS"
