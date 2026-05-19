from usa_signal_bot.release_packaging.packaging_models import VersionedCandidateBundle, create_versioned_candidate_bundle_id
from usa_signal_bot.core.enums import ReleaseBundleType, ReleaseBundleStatus

def test_versioned_candidate_bundle_valid():
    bundle = VersionedCandidateBundle(
        bundle_id=create_versioned_candidate_bundle_id(),
        created_at_utc="2023-01-01T00:00:00Z",
        bundle_version="0.1.0",
        bundle_type=ReleaseBundleType.LOCAL_RESEARCH_CANDIDATE,
        status=ReleaseBundleStatus.DRAFT,
        title="Test",
        description="Test",
        source_candidate_id=None,
        source_experiment_id=None,
        source_hypothesis_id=None,
        source_governance_review_id=None,
        manifest=None,
        validation_result=None,
        bundle_path=None,
        readme_path=None,
        allowed_for_auto_apply=False,
        allowed_for_live_or_demo_execution=False,
        allowed_for_order_routing=False,
        warnings=[],
        errors=[]
    )
    assert bundle.allowed_for_auto_apply is False
