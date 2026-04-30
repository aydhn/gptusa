import pytest
from usa_signal_bot.data.batches import build_symbol_batch_objects, estimate_large_universe_runtime

def test_build_symbol_batch_objects():
    symbols = ["A", "B", "C", "D", "E"]

    batches = build_symbol_batch_objects(symbols, batch_size=2)
    assert len(batches) == 3
    assert batches[0].symbols == ["A", "B"]
    assert batches[0].index == 0
    assert batches[0].total_batches == 3
    assert batches[2].symbols == ["E"]

def test_build_symbol_batch_objects_invalid():
    with pytest.raises(ValueError):
        build_symbol_batch_objects(["A"], 0)

def test_estimate_large_universe_runtime():
    est = estimate_large_universe_runtime(
        symbol_count=1000,
        timeframe_count=3,
        min_seconds_between_requests=1.0,
        batch_size=100
    )

    assert est["symbol_count"] == 1000
    assert est["total_requests"] == 3000
    assert est["total_batches"] == 10
    # Wait time = 3000 * 1.0 = 3000
    # Download time ~ 3000 * 2.0 = 6000
    assert est["total_estimated_seconds"] == 9000
