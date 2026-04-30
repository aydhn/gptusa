import pytest
from unittest.mock import patch, MagicMock
from usa_signal_bot.app.cli import (
    handle_indicator_list,
    handle_indicator_info,
    handle_feature_store_info,
    handle_feature_summary,
    handle_feature_compute_cache
)

@pytest.fixture
def mock_context():
    ctx = MagicMock()
    cfg = MagicMock()
    cfg.features.default_indicators = ["close_return"]
    cfg.features.default_storage_format = "jsonl"
    ctx.config = cfg
    ctx.data_dir = Path("/tmp/data")
    return ctx

from pathlib import Path

def test_handle_indicator_list(mock_context):
    assert handle_indicator_list(mock_context) == 0

def test_handle_indicator_info(mock_context):
    assert handle_indicator_info(mock_context, "close_sma") == 0
    assert handle_indicator_info(mock_context, "unknown") == 1

def test_handle_feature_store_info(mock_context):
    # Fails if path doesn't exist? Actually feature_store_dir creates it.
    with patch("usa_signal_bot.features.feature_store.feature_store_dir") as mock_dir:
        mock_dir.return_value.glob.return_value = []
        assert handle_feature_store_info(mock_context) == 0

def test_handle_feature_summary(mock_context):
    with patch("usa_signal_bot.features.feature_store.feature_store_dir") as mock_dir:
        mock_dir.return_value.glob.return_value = []
        assert handle_feature_summary(mock_context) == 0

def test_handle_feature_compute_cache_empty(mock_context):
    # Cache is empty so it will fail
    with patch("usa_signal_bot.features.engine.FeatureEngine.compute_from_cache") as mock_compute:
        mock_res = MagicMock()
        mock_res.feature_rows = []
        mock_res.is_successful.return_value = False
        mock_compute.return_value = mock_res

        assert handle_feature_compute_cache(mock_context, "AAPL", "1d", "close_return", "yfinance", False) == 1
