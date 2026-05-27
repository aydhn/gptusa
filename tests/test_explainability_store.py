import pytest
from usa_signal_bot.feature_engine.factor_explainability.explainability_store import explainability_store_summary

def test_explainability_store_summary(tmp_path):
    res = explainability_store_summary(tmp_path)
    assert "reviews_count" in res
