import pytest
from usa_signal_bot.backtesting.benchmark_comparison.passive_benchmark_config import (
    build_default_passive_benchmark_config
)

def test_build_passive_benchmark_config():
    config = build_default_passive_benchmark_config(100000.0)
    assert config.config_valid is True
    assert config.initial_cash == 100000.0
    assert config.external_benchmark_fetch_enabled is False
    assert config.equal_weight_metadata_only is True
