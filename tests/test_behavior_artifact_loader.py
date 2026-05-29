from usa_signal_bot.regime_classification.alignment.behavior_artifact_loader import validate_behavior_artifacts
def test_validate_behavior_artifacts():
    errs = validate_behavior_artifacts({"msg": "this is investment advice!"})
    assert len(errs) > 0
