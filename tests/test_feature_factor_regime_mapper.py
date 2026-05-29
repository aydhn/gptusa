from usa_signal_bot.regime_classification.alignment.feature_factor_regime_mapper import map_factor_columns_to_regime_context
from usa_signal_bot.regime_classification.alignment.alignment_specs import build_default_regime_alignment_specs
from usa_signal_bot.regime_classification.alignment.phase131_models import FrozenFactorAlignmentReference
def test_mapper():
    ref = FrozenFactorAlignmentReference(reference_id="r1", created_at_utc="", symbol="AAPL", artifact_name="", artifact_path="", artifact_hash="", factor_columns=["f1"], available=True)
    specs = build_default_regime_alignment_specs()
    res = map_factor_columns_to_regime_context([ref], [{"symbol": "AAPL"}], specs)
    assert len(res) > 0
