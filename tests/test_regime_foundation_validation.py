from usa_signal_bot.regime_classification.foundation.regime_foundation_validation import validate_no_unsafe_regime_foundation_fields

def test_validate_no_unsafe_regime_foundation_fields():
    rep = validate_no_unsafe_regime_foundation_fields({"safe_key": "safe_val"})
    assert rep.valid is True

    rep = validate_no_unsafe_regime_foundation_fields({"activation_allowed": True})
    assert rep.valid is False
    assert rep.blocked_count == 1

    rep = validate_no_unsafe_regime_foundation_fields({"some_key": "buy_signal"})
    assert rep.valid is False
    assert rep.blocked_count == 1
