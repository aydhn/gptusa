from usa_signal_bot.regime_classification.freeze_preparation.degradation_consistency_validator import validate_degradation_recommended_actions

def test_validate_degradation_recommended_actions():
    errs = validate_degradation_recommended_actions([{"recommended_action_type": "research_review"}])
    assert len(errs) == 0
    errs = validate_degradation_recommended_actions([{"recommended_action_type": "buy_now"}])
    assert len(errs) == 1
