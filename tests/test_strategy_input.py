import pytest
from usa_signal_bot.strategies.strategy_input import StrategyFeatureFrame, StrategyInputBatch, validate_strategy_feature_frame, filter_valid_strategy_frames

def test_strategy_input_validation():
    frame = StrategyFeatureFrame(
        symbol="AAPL",
        timeframe="1d",
        rows=[{"f1": 1}],
        feature_names=["f1"]
    )

    res = validate_strategy_feature_frame(frame, ["f1"])
    assert res.valid

    res = validate_strategy_feature_frame(frame, ["f1", "f2"])
    assert not res.valid
    assert "f2" in res.missing_required_features

def test_strategy_input_filter():
    f1 = StrategyFeatureFrame(symbol="AAPL", timeframe="1d", rows=[{"f1": 1}], feature_names=["f1"])
    f2 = StrategyFeatureFrame(symbol="MSFT", timeframe="1d", rows=[], feature_names=[])

    batch = StrategyInputBatch(frames=[f1, f2], provider_name="test", symbols=["AAPL", "MSFT"], timeframes=["1d"], created_at_utc="test")

    # Fake validation results
    from usa_signal_bot.strategies.strategy_input import StrategyInputValidationResult
    v1 = StrategyInputValidationResult(valid=True, symbol="AAPL", timeframe="1d", row_count=1, missing_required_features=[], messages=[])
    v2 = StrategyInputValidationResult(valid=False, symbol="MSFT", timeframe="1d", row_count=0, missing_required_features=["f1"], messages=[])

    filtered = filter_valid_strategy_frames(batch, [v1, v2])
    assert len(filtered.frames) == 1
    assert filtered.frames[0].symbol == "AAPL"
