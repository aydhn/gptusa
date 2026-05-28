import pytest
from usa_signal_bot.regime_classification.feature_engineering.regime_feature_engineering_report import (
    build_regime_feature_engineering_full_review
)

def test_build_regime_feature_engineering_full_review():
    rev = build_regime_feature_engineering_full_review()
    assert rev is not None
