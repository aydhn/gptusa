from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_package_builder import build_required_research_freeze_artifact_kinds

def test_build_required_research_freeze_artifact_kinds():
    kinds = build_required_research_freeze_artifact_kinds()
    assert len(kinds) == 10
