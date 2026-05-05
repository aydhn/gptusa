import pytest
from usa_signal_bot.core.enums import ParameterValueType, ParameterGridType
from usa_signal_bot.backtesting.parameter_sensitivity_models import ParameterRangeSpec
from usa_signal_bot.backtesting.parameter_grid import (
    create_single_parameter_grid, create_two_parameter_grid,
    create_multi_parameter_grid, create_local_neighborhood_grid,
    infer_parameter_value_type, estimate_grid_cell_count,
    create_parameter_grid_cells, limit_grid_cells, grid_cells_to_text,
    validate_grid_against_strategy_schema
)
from usa_signal_bot.strategies.strategy_params import StrategyParameterSchema, StrategyParameterSpec

def test_infer_parameter_value_type():
    assert infer_parameter_value_type([1, 2]) == ParameterValueType.INT
    assert infer_parameter_value_type([1.5, 2.0]) == ParameterValueType.FLOAT
    assert infer_parameter_value_type([True, False]) == ParameterValueType.BOOL
    assert infer_parameter_value_type(["a", "b"]) == ParameterValueType.STR

def test_estimate_grid_cell_count():
    spec1 = ParameterRangeSpec("a", ParameterValueType.INT, [1, 2])
    spec2 = ParameterRangeSpec("b", ParameterValueType.INT, [3, 4, 5])
    assert estimate_grid_cell_count([spec1, spec2]) == 6

def test_create_single_parameter_grid():
    grid = create_single_parameter_grid("test_strat", "a", [1, 2], ParameterValueType.INT)
    assert grid.grid_type == ParameterGridType.SINGLE_PARAMETER
    assert len(grid.parameters) == 1

    cells = create_parameter_grid_cells(grid)
    assert len(cells) == 2
    assert cells[0].params == {"a": 1}
    assert cells[1].params == {"a": 2}

def test_create_two_parameter_grid():
    spec1 = ParameterRangeSpec("a", ParameterValueType.INT, [1, 2])
    spec2 = ParameterRangeSpec("b", ParameterValueType.INT, [3, 4])
    grid = create_two_parameter_grid("test_strat", spec1, spec2)
    assert grid.grid_type == ParameterGridType.TWO_PARAMETER

    cells = create_parameter_grid_cells(grid)
    assert len(cells) == 4

def test_create_multi_parameter_grid():
    spec1 = ParameterRangeSpec("a", ParameterValueType.INT, [1, 2])
    spec2 = ParameterRangeSpec("b", ParameterValueType.INT, [3, 4])
    spec3 = ParameterRangeSpec("c", ParameterValueType.INT, [5, 6])
    grid = create_multi_parameter_grid("test_strat", [spec1, spec2, spec3])

    cells = create_parameter_grid_cells(grid)
    assert len(cells) == 8
    # Deterministic output verification
    assert cells[0].params == {"a": 1, "b": 3, "c": 5}
    assert cells[-1].params == {"a": 2, "b": 4, "c": 6}

def test_create_local_neighborhood_grid():
    base = {"a": 10, "b": 20}
    pert = {"a": [9, 10, 11], "b": [19, 20, 21]}
    grid = create_local_neighborhood_grid("test_strat", base, pert)
    cells = create_parameter_grid_cells(grid)
    assert len(cells) == 9

def test_limit_grid_cells():
    grid = create_single_parameter_grid("test_strat", "a", [1, 2, 3, 4, 5], ParameterValueType.INT, max_cells=3)
    cells = create_parameter_grid_cells(grid)
    assert len(cells) == 3

def test_validate_grid_against_strategy_schema():
    schema = StrategyParameterSchema("test_strat", parameters=[
        StrategyParameterSpec("a", "int", 5, min_value=1, max_value=10)
    ])
    grid_ok = create_single_parameter_grid("test", "a", [1, 5, 10], ParameterValueType.INT)
    assert not validate_grid_against_strategy_schema(grid_ok, schema)

    grid_bad = create_single_parameter_grid("test", "a", [11], ParameterValueType.INT)
    errors = validate_grid_against_strategy_schema(grid_bad, schema)
    assert len(errors) == 1
    assert "not allowed" in errors[0]

    grid_unknown = create_single_parameter_grid("test", "unknown", [1], ParameterValueType.INT)
    errors2 = validate_grid_against_strategy_schema(grid_unknown, schema)
    assert len(errors2) == 1
    assert "Unknown parameter" in errors2[0]

def test_grid_cells_to_text():
    grid = create_single_parameter_grid("test", "a", [1, 2], ParameterValueType.INT)
    cells = create_parameter_grid_cells(grid)
    txt = grid_cells_to_text(cells)
    assert "Total Cells: 2" in txt
