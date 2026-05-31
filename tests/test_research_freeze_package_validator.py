from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_package_validator import validate_research_freeze_artifact_references
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import ResearchFreezeArtifactReference, ResearchFreezeArtifactKind

def test_validate_research_freeze_artifact_references():
    ref = ResearchFreezeArtifactReference("r1", "", ResearchFreezeArtifactKind.DRIFT_REPORT, "DRIFT", 134, None, None, None, True, True, True, True, False, False, False, False, [], [], [])
    errs = validate_research_freeze_artifact_references([ref])
    # Expect errors because it's missing the other 9
    assert len(errs) == 9
