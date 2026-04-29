import pytest
from usa_signal_bot.data.batches import (
    validate_batch_size, chunk_symbols, estimate_batch_count, build_symbol_batches
)
from usa_signal_bot.core.exceptions import DataValidationError

def test_validate_batch_size():
    validate_batch_size(10)
    with pytest.raises(DataValidationError):
        validate_batch_size(0)
    with pytest.raises(DataValidationError):
        validate_batch_size(-5)

def test_chunk_symbols():
    symbols = ["A", "B", "C", "D", "E"]
    chunks = chunk_symbols(symbols, 2)
    assert len(chunks) == 3
    assert chunks[0] == ["A", "B"]
    assert chunks[1] == ["C", "D"]
    assert chunks[2] == ["E"]

def test_estimate_batch_count():
    assert estimate_batch_count(["A", "B", "C"], 2) == 2
    assert estimate_batch_count([], 2) == 0

def test_build_symbol_batches():
    symbols = ["a", "b", "A", "", " c "]

    # Deduplicate true
    batches = build_symbol_batches(symbols, 2, deduplicate=True)
    assert batches == [["A", "B"], ["C"]]

    # Deduplicate false
    batches2 = build_symbol_batches(symbols, 2, deduplicate=False)
    assert batches2 == [["A", "B"], ["A", "C"]]
