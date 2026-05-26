import pytest
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_report import build_advanced_feature_full_review

def test_report():
    r = build_advanced_feature_full_review()
    assert r.review_id is not None
