import itertools
import uuid
from typing import Any
from usa_signal_bot.core.enums import ParameterGridType, ParameterValueType
from usa_signal_bot.core.exceptions import ParameterGridError
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterRangeSpec, ParameterGridSpec, ParameterGridCell
)
from usa_signal_bot.strategies.strategy_params import StrategyParameterSchema, is_parameter_value_allowed

def infer_parameter_value_type(values: list[Any]) -> ParameterValueType:
    if not values:
        return ParameterValueType.STR
    first_val = values[0]
    if isinstance(first_val, bool):
        return ParameterValueType.BOOL
    if isinstance(first_val, int):
        return ParameterValueType.INT
    if isinstance(first_val, float):
        return ParameterValueType.FLOAT
    return ParameterValueType.STR

def estimate_grid_cell_count(parameters: list[ParameterRangeSpec]) -> int:
    count = 1
    for p in parameters:
        count *= len(p.values)
    return count

def create_parameter_grid_cells(grid_spec: ParameterGridSpec) -> list[ParameterGridCell]:
    keys = [p.name for p in grid_spec.parameters]
    value_lists = [p.values for p in grid_spec.parameters]

    cells = []
    for idx, combo in enumerate(itertools.product(*value_lists)):
        params = dict(zip(keys, combo))
        cells.append(ParameterGridCell(
            cell_id=f"cell_{idx:04d}",
            index=idx,
            strategy_name=grid_spec.strategy_name,
            params=params
        ))

        if len(cells) >= grid_spec.max_cells:
            break

    return cells

def create_single_parameter_grid(
    strategy_name: str,
    parameter_name: str,
    values: list[Any],
    value_type: ParameterValueType,
    max_cells: int = 100
) -> ParameterGridSpec:
    spec = ParameterRangeSpec(name=parameter_name, value_type=value_type, values=values)
    grid_spec = ParameterGridSpec(
        grid_id=f"grid_single_{uuid.uuid4().hex[:8]}",
        strategy_name=strategy_name,
        grid_type=ParameterGridType.SINGLE_PARAMETER,
        parameters=[spec],
        max_cells=max_cells
    )
    return grid_spec

def create_two_parameter_grid(
    strategy_name: str,
    param_a: ParameterRangeSpec,
    param_b: ParameterRangeSpec,
    max_cells: int = 500
) -> ParameterGridSpec:
    grid_spec = ParameterGridSpec(
        grid_id=f"grid_two_{uuid.uuid4().hex[:8]}",
        strategy_name=strategy_name,
        grid_type=ParameterGridType.TWO_PARAMETER,
        parameters=[param_a, param_b],
        max_cells=max_cells
    )
    return grid_spec

def create_multi_parameter_grid(
    strategy_name: str,
    parameters: list[ParameterRangeSpec],
    max_cells: int = 1000
) -> ParameterGridSpec:
    grid_spec = ParameterGridSpec(
        grid_id=f"grid_multi_{uuid.uuid4().hex[:8]}",
        strategy_name=strategy_name,
        grid_type=ParameterGridType.MULTI_PARAMETER,
        parameters=parameters,
        max_cells=max_cells
    )
    return grid_spec

def create_local_neighborhood_grid(
    strategy_name: str,
    base_params: dict[str, Any],
    perturbations: dict[str, list[Any]],
    max_cells: int = 500
) -> ParameterGridSpec:
    parameters = []
    for p_name, p_vals in perturbations.items():
        val_type = infer_parameter_value_type(p_vals)
        parameters.append(ParameterRangeSpec(name=p_name, value_type=val_type, values=p_vals, default_value=base_params.get(p_name)))

    grid_spec = ParameterGridSpec(
        grid_id=f"grid_local_{uuid.uuid4().hex[:8]}",
        strategy_name=strategy_name,
        grid_type=ParameterGridType.LOCAL_NEIGHBORHOOD,
        parameters=parameters,
        max_cells=max_cells,
        metadata={"base_params": base_params}
    )
    return grid_spec

def validate_grid_against_strategy_schema(grid_spec: ParameterGridSpec, parameter_schema: StrategyParameterSchema) -> list[str]:
    from usa_signal_bot.strategies.strategy_params import get_parameter_spec
    errors = []
    for param in grid_spec.parameters:
        spec = get_parameter_spec(parameter_schema, param.name)
        if not spec:
            errors.append(f"Unknown parameter '{param.name}' not found in strategy schema.")
            continue

        for val in param.values:
            if not is_parameter_value_allowed(spec, val):
                errors.append(f"Value {val} is not allowed for parameter '{param.name}' according to schema.")
    return errors

def limit_grid_cells(cells: list[ParameterGridCell], max_cells: int) -> list[ParameterGridCell]:
    return cells[:max_cells]

def grid_cells_to_text(cells: list[ParameterGridCell], limit: int = 20) -> str:
    lines = [f"Total Cells: {len(cells)}"]
    display_cells = cells[:limit]
    for cell in display_cells:
        lines.append(f"  [{cell.cell_id}] index={cell.index} params={cell.params}")
    if len(cells) > limit:
        lines.append(f"  ... and {len(cells) - limit} more cells.")
    return "\n".join(lines)
