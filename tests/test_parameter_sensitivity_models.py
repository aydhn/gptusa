import pytest
from usa_signal_bot.core.enums import ParameterValueType, ParameterGridType
from usa_signal_bot.core.exceptions import ParameterGridError
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterRangeSpec, ParameterGridSpec, ParameterGridCell,
    validate_parameter_range_spec, validate_parameter_grid_spec,
    create_sensitivity_run_id, parameter_grid_cell_to_dict
)

def test_parameter_range_spec_valid():
    spec = ParameterRangeSpec("min_score", ParameterValueType.INT, [1, 2, 3])
    validate_parameter_range_spec(spec)
    assert spec.name == "min_score"

def test_parameter_range_spec_invalid_empty_values():
    spec = ParameterRangeSpec("min_score", ParameterValueType.INT, [])
    with pytest.raises(ParameterGridError, match="cannot be empty"):
        validate_parameter_range_spec(spec)

def test_parameter_range_spec_invalid_type():
    spec = ParameterRangeSpec("min_score", ParameterValueType.INT, [1, "two", 3])
    with pytest.raises(ParameterGridError, match="must be int"):
        validate_parameter_range_spec(spec)

def test_parameter_grid_spec_valid():
    spec1 = ParameterRangeSpec("a", ParameterValueType.INT, [1, 2])
    grid = ParameterGridSpec("g1", "strat_a", ParameterGridType.SINGLE_PARAMETER, [spec1], 100)
    validate_parameter_grid_spec(grid)
    assert grid.grid_id == "g1"

def test_parameter_grid_spec_invalid_max_cells():
    spec1 = ParameterRangeSpec("a", ParameterValueType.INT, [1, 2])
    grid = ParameterGridSpec("g1", "strat_a", ParameterGridType.SINGLE_PARAMETER, [spec1], 0)
    with pytest.raises(ParameterGridError, match="max_cells must be positive"):
        validate_parameter_grid_spec(grid)

def test_create_sensitivity_run_id():
    run_id = create_sensitivity_run_id("test")
    assert run_id.startswith("sens_test_")
    assert len(run_id) > 10

def test_parameter_grid_cell_serialization():
    cell = ParameterGridCell("c1", 0, "strat", {"a": 1})
    d = parameter_grid_cell_to_dict(cell)
    assert d["cell_id"] == "c1"
    assert d["params"] == {"a": 1}
