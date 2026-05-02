import pytest
from usa_signal_bot.core.enums import StrategyCategory, StrategyStatus, SignalAction
from usa_signal_bot.strategies.strategy_metadata import StrategyMetadata, validate_strategy_metadata, strategy_metadata_to_dict, strategy_metadata_summary_text
from usa_signal_bot.core.exceptions import StrategyMetadataError

def test_strategy_metadata_valid():
    m = StrategyMetadata(
        name="test_strat",
        version="1.0.0",
        category=StrategyCategory.TREND_FOLLOWING,
        status=StrategyStatus.EXPERIMENTAL,
        description="A test strat",
        required_features=["f1"],
        produces_actions=[SignalAction.WATCH]
    )
    validate_strategy_metadata(m) # should not raise

def test_strategy_metadata_invalid_name():
    m = StrategyMetadata(
        name="",
        version="1.0.0",
        category=StrategyCategory.TREND_FOLLOWING,
        status=StrategyStatus.EXPERIMENTAL,
        description="A test strat",
        required_features=["f1"],
        produces_actions=[SignalAction.WATCH]
    )
    with pytest.raises(StrategyMetadataError):
        validate_strategy_metadata(m)

def test_strategy_metadata_empty_actions():
    m = StrategyMetadata(
        name="test_strat",
        version="1.0.0",
        category=StrategyCategory.TREND_FOLLOWING,
        status=StrategyStatus.EXPERIMENTAL,
        description="A test strat",
        required_features=["f1"],
        produces_actions=[]
    )
    with pytest.raises(StrategyMetadataError):
        validate_strategy_metadata(m)

def test_strategy_metadata_dict_and_text():
    m = StrategyMetadata(
        name="test_strat",
        version="1.0.0",
        category=StrategyCategory.TREND_FOLLOWING,
        status=StrategyStatus.EXPERIMENTAL,
        description="A test strat",
        required_features=["f1"],
        produces_actions=[SignalAction.WATCH]
    )
    d = strategy_metadata_to_dict(m)
    assert d["name"] == "test_strat"
    assert d["category"] == "TREND_FOLLOWING"

    t = strategy_metadata_summary_text(m)
    assert "Strategy: test_strat (v1.0.0)" in t
