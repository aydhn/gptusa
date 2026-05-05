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

def test_get_parameter_spec():
    from usa_signal_bot.strategies.strategy_params import get_parameter_spec, StrategyParameterSchema, StrategyParameterSpec
    schema = StrategyParameterSchema("test", parameters=[
        StrategyParameterSpec("a", "int", 5)
    ])
    spec = get_parameter_spec(schema, "a")
    assert spec is not None
    assert spec.name == "a"

    spec2 = get_parameter_spec(schema, "b")
    assert spec2 is None

def test_strategy_schema_parameter_names():
    from usa_signal_bot.strategies.strategy_params import strategy_schema_parameter_names, StrategyParameterSchema, StrategyParameterSpec
    schema = StrategyParameterSchema("test", parameters=[
        StrategyParameterSpec("a", "int", 5),
        StrategyParameterSpec("b", "float", 1.0)
    ])
    assert strategy_schema_parameter_names(schema) == ["a", "b"]

def test_is_parameter_value_allowed():
    from usa_signal_bot.strategies.strategy_params import is_parameter_value_allowed, StrategyParameterSpec
    spec = StrategyParameterSpec("a", "int", 5, min_value=1, max_value=10, allowed_values=[1, 5, 10])
    assert is_parameter_value_allowed(spec, 5)
    assert not is_parameter_value_allowed(spec, 6) # Not in allowed_values

    spec2 = StrategyParameterSpec("b", "int", 5, min_value=1, max_value=10)
    assert is_parameter_value_allowed(spec2, 5)
    assert not is_parameter_value_allowed(spec2, 11)
    assert not is_parameter_value_allowed(spec2, 0)

def test_coerce_parameter_value():
    from usa_signal_bot.strategies.strategy_params import coerce_parameter_value
    assert coerce_parameter_value("1", "int") == 1
    assert coerce_parameter_value("1.5", "float") == 1.5
    assert coerce_parameter_value("True", "bool") is True
    assert coerce_parameter_value("false", "bool") is False
    assert coerce_parameter_value(1, "str") == "1"
