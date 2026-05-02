import pytest
from usa_signal_bot.strategies.strategy_params import StrategyParameterSpec, StrategyParameterSchema, validate_strategy_params, validate_strategy_parameter_schema
from usa_signal_bot.core.exceptions import StrategyParameterError

def test_strategy_params_valid():
    s = StrategyParameterSchema(
        strategy_name="test",
        parameters=[
            StrategyParameterSpec(name="p1", param_type="int", default=10, min_value=5, max_value=20)
        ]
    )
    validate_strategy_parameter_schema(s)

    merged = validate_strategy_params(s, {"p1": 15})
    assert merged["p1"] == 15

    merged2 = validate_strategy_params(s)
    assert merged2["p1"] == 10

def test_strategy_params_missing_required():
    s = StrategyParameterSchema(
        strategy_name="test",
        parameters=[
            StrategyParameterSpec(name="p1", param_type="int", default=None, required=True)
        ]
    )
    with pytest.raises(StrategyParameterError):
        validate_strategy_params(s)

def test_strategy_params_invalid_type():
    s = StrategyParameterSchema(
        strategy_name="test",
        parameters=[
            StrategyParameterSpec(name="p1", param_type="int", default=10)
        ]
    )
    with pytest.raises(StrategyParameterError):
        validate_strategy_params(s, {"p1": "15"})

def test_strategy_params_out_of_bounds():
    s = StrategyParameterSchema(
        strategy_name="test",
        parameters=[
            StrategyParameterSpec(name="p1", param_type="int", default=10, max_value=20)
        ]
    )
    with pytest.raises(StrategyParameterError):
        validate_strategy_params(s, {"p1": 25})

def test_strategy_params_extra_param():
    s = StrategyParameterSchema(
        strategy_name="test",
        parameters=[
            StrategyParameterSpec(name="p1", param_type="int", default=10)
        ]
    )
    with pytest.raises(StrategyParameterError):
        validate_strategy_params(s, {"p2": 5})
