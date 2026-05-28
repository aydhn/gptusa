from usa_signal_bot.regime_classification.foundation.regime_label_taxonomy import build_regime_label_taxonomy
from usa_signal_bot.regime_classification.foundation.regime_taxonomy_validator import validate_regime_taxonomy

def test_validate_regime_taxonomy_valid():
    tax = build_regime_label_taxonomy()
    errors = validate_regime_taxonomy(tax)
    assert len(errors) == 0

def test_validate_regime_taxonomy_invalid_activation():
    tax = build_regime_label_taxonomy()
    tax.activation_allowed = True
    errors = validate_regime_taxonomy(tax)
    assert len(errors) == 1
    assert "allows activation" in errors[0]
