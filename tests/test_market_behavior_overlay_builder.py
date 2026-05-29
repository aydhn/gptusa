from usa_signal_bot.regime_classification.alignment.market_behavior_overlay_builder import build_market_behavior_overlays
from usa_signal_bot.regime_classification.alignment.alignment_specs import build_default_market_behavior_overlay_specs
from usa_signal_bot.regime_classification.alignment.phase131_models import FrozenFactorAlignmentReference
def test_builder():
    ref = FrozenFactorAlignmentReference(reference_id="r1", created_at_utc="", symbol="AAPL", artifact_name="", artifact_path="", artifact_hash="", factor_columns=["f1"], available=True)
    specs = build_default_market_behavior_overlay_specs()
    res = build_market_behavior_overlays([ref], [{"symbol": "AAPL"}], specs)
    assert len(res) > 0
