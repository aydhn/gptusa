from usa_signal_bot.regime_classification.foundation.regime_label_taxonomy import build_regime_label_taxonomy, compute_regime_taxonomy_hash
from usa_signal_bot.core.enums import RegimeTaxonomyStatus

def test_build_regime_label_taxonomy():
    tax = build_regime_label_taxonomy()
    assert tax.status == RegimeTaxonomyStatus.CREATED
    assert tax.label_count >= 13
    assert tax.unknown_label == "unknown_regime"
    assert tax.default_label == "unknown_regime"
    assert tax.taxonomy_hash is not None
    assert tax.activation_allowed is False

def test_taxonomy_hash_consistency():
    tax1 = build_regime_label_taxonomy()
    tax2 = build_regime_label_taxonomy()
    assert tax1.taxonomy_hash == tax2.taxonomy_hash
