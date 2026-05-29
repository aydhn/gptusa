from usa_signal_bot.regime_classification.alignment.compatibility_engine import compute_regime_context_compatibility
from usa_signal_bot.regime_classification.alignment.alignment_specs import build_default_regime_alignment_specs
from usa_signal_bot.regime_classification.alignment.phase131_models import FrozenFactorAlignmentReference
def test_engine():
    ref = FrozenFactorAlignmentReference(reference_id="r1", created_at_utc="", symbol="AAPL", artifact_name="", artifact_path="", artifact_hash="", factor_columns=["f1"], available=True)
    specs = build_default_regime_alignment_specs()
    res = compute_regime_context_compatibility([ref], [{"symbol": "AAPL"}], None, specs)
    assert len(res) > 0
