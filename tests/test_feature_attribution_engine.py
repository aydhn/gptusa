import pytest
import pandas as pd
from usa_signal_bot.feature_engine.factor_explainability.attribution_specs import build_attribution_spec_for_factor
from usa_signal_bot.feature_engine.factor_explainability.feature_attribution_engine import build_feature_attributions_for_symbol

def test_build_feature_attributions_for_symbol():
    df = pd.DataFrame({"mom_10": [1,2,3], "mom_5": [1,2,2]})
    spec = build_attribution_spec_for_factor("mom_10", "mom_10", ["mom_5"])
    res = build_feature_attributions_for_symbol("AAPL", df, [spec])
    assert len(res) == 1
    assert 0 <= res[0].attribution_score <= 100
    assert 0 <= res[0].normalized_attribution_score <= 1
    assert res[0].produces_trade_signal is False
