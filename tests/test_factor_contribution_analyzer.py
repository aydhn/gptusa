import pytest
from usa_signal_bot.core.enums import AttributionDirection
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import FeatureAttributionResult
from usa_signal_bot.feature_engine.factor_explainability.factor_contribution_analyzer import build_factor_contribution_profile

def test_build_factor_contribution_profile():
    attrs = [
        FeatureAttributionResult("i", "", "AAPL", "mom", "mom", "feat1", 60.0, 0.6, AttributionDirection.POSITIVE_CONTEXT, "DETERMINISTIC_HEURISTIC", None, None, None, None, "", True, False, False, False, [], [], [], {})
    ]
    prof = build_factor_contribution_profile("AAPL", "mom", "mom", attrs)
    assert prof.produces_trade_signal is False
    assert len(prof.top_positive_features) == 1
