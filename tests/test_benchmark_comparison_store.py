import pytest
from pathlib import Path
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_comparison_store import (
    benchmark_comparison_store_dir
)

def test_store_dir(tmp_path):
    d = benchmark_comparison_store_dir(tmp_path)
    assert d.exists()
