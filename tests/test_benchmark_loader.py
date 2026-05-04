import pytest
from pathlib import Path
from usa_signal_bot.backtesting.benchmark_loader import (
    default_benchmark_specs, default_benchmark_set, get_benchmark_set, list_benchmark_sets,
    load_benchmark_market_data_from_cache, validate_benchmark_cache_coverage
)
from usa_signal_bot.core.enums import BenchmarkType
from usa_signal_bot.core.exceptions import BenchmarkLoaderError
from usa_signal_bot.data.models import OHLCVBar

def test_default_benchmark_specs():
    specs = default_benchmark_specs()
    assert len(specs) == 4
    symbols = [s.symbol for s in specs]
    assert "SPY" in symbols
    assert "CASH" in symbols

def test_default_benchmark_set():
    bset = default_benchmark_set()
    assert bset.name == "default"
    assert len(bset.benchmarks) == 4

def test_get_benchmark_set():
    bset = get_benchmark_set("broad_market")
    assert bset.name == "broad_market"

    with pytest.raises(BenchmarkLoaderError):
        get_benchmark_set("unknown_set")

def test_validate_benchmark_cache_coverage():
    bset = default_benchmark_set()
    # Missing SPY, QQQ, IWM. CASH doesn't need cache.
    data = {}
    msgs = validate_benchmark_cache_coverage(data, bset)
    assert len(msgs) == 3

    # Empty data
    data = {"SPY": [], "QQQ": [], "IWM": []}
    msgs = validate_benchmark_cache_coverage(data, bset)
    assert len(msgs) == 3
    assert "empty" in msgs[0]

def test_load_benchmark_market_data_from_cache(tmp_path):
    bset = default_benchmark_set()
    # If no data exists, it shouldn't fail, it just returns empty dict or partial
    data = load_benchmark_market_data_from_cache(tmp_path, bset, "1d")
    assert isinstance(data, dict)
