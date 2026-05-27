import pytest
from usa_signal_bot.feature_engine.factor_explainability.attribution_specs import build_attribution_spec_for_factor

def test_build_attribution_spec_for_factor():
    spec = build_attribution_spec_for_factor("mom_10", "mom_10", ["mom_5", "vol_10"])
    assert spec.produces_trade_signal is False
    assert spec.factor_name == "mom_10"
