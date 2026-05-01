import pytest
from pathlib import Path
from usa_signal_bot.features.engine import FeatureEngine
from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
from usa_signal_bot.features.input_contract import FeatureInput, FeatureBatchInput
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.core.enums import FeatureComputationStatus

@pytest.fixture
def registry():
    return create_default_indicator_registry()

@pytest.fixture
def fake_input():
    bars = [
        OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc="2023-01-01", open=10, high=11, low=9, close=10, volume=100),
        OHLCVBar(symbol="AAPL", timeframe="1d", timestamp_utc="2023-01-02", open=10, high=11, low=9, close=11, volume=100)
    ]
    return FeatureInput("AAPL", "1d", bars)

def test_engine_compute_for_input(registry, tmp_path, fake_input):
    engine = FeatureEngine(registry, tmp_path)

    res = engine.compute_for_input(fake_input, ["close_return"])
    assert res.is_successful()
    assert len(res.feature_rows) == 2
    assert "close_return_1" in res.produced_features
    assert not res.errors

def test_engine_compute_for_batch(registry, tmp_path, fake_input):
    engine = FeatureEngine(registry, tmp_path)

    batch = FeatureBatchInput([fake_input], "2023", "test")
    res = engine.compute_for_batch(batch, ["close_return"])

    assert res.is_successful()
    assert len(res.feature_rows) == 2

def test_engine_unknown_indicator(registry, tmp_path, fake_input):
    engine = FeatureEngine(registry, tmp_path)
    res = engine.compute_for_input(fake_input, ["unknown"])

    # Empty produced features -> failed
    assert res.status == FeatureComputationStatus.FAILED
    assert len(res.errors) == 1
    assert "not found in registry" in res.errors[0]

def test_engine_write_result(registry, tmp_path, fake_input):
    engine = FeatureEngine(registry, tmp_path)
    res = engine.compute_for_input(fake_input, ["close_return"])

    meta = engine.write_result(res)
    assert meta.row_count == 2
    assert len(meta.storage_paths) == 1
    assert Path(meta.storage_paths[0]).exists()

def test_engine_compute_from_cache(registry, tmp_path):
    engine = FeatureEngine(registry, tmp_path)

    # Just check it returns gracefully on empty cache
    res = engine.compute_from_cache(["AAPL"], ["1d"], ["close_return"])
    # Batch would be empty, valid inputs empty
    # Engine will return FAILED because no rows produced and no valid symbols
    assert res.status == FeatureComputationStatus.COMPLETED

def test_engine_compute_momentum_set_for_input(registry, tmp_path, fake_input):
    from usa_signal_bot.features.engine import FeatureEngine
    engine = FeatureEngine(registry, tmp_path)
    res = engine.compute_momentum_set_for_input(fake_input, "basic_momentum")
    assert res.is_successful()

def test_engine_compute_momentum_set_for_batch(registry, tmp_path, fake_input):
    from usa_signal_bot.features.engine import FeatureEngine
    from usa_signal_bot.features.input_contract import FeatureBatchInput
    engine = FeatureEngine(registry, tmp_path)
    batch = FeatureBatchInput([fake_input], "2023", "test")
    res = engine.compute_momentum_set_for_batch(batch, "oscillator_momentum")
    assert res.is_successful()
