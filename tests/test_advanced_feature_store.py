import pytest
from pathlib import Path
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_store import advanced_feature_store_summary

def test_store(tmp_path):
    s = advanced_feature_store_summary(tmp_path)
    assert s["reviews"] == 0
