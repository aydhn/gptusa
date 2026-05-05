from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import (
    ParameterGridType,
    ParameterValueType,
    SensitivityRunStatus,
    SensitivityCellStatus,
    StabilityBucket,
    ParameterZoneType,
    OverfitRiskHint,
    SensitivityMetricName
)

@dataclass
class ParameterRangeSpec:
    name: str
    value_type: ParameterValueType
    values: list[Any]
    default_value: Any | None = None
    description: str | None = None

@dataclass
class ParameterGridSpec:
    grid_id: str
    strategy_name: str
    grid_type: ParameterGridType
    parameters: list[ParameterRangeSpec]
    max_cells: int
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ParameterGridCell:
    cell_id: str
    index: int
    strategy_name: str
    params: dict[str, Any]
    status: SensitivityCellStatus = SensitivityCellStatus.NOT_RUN
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ParameterSensitivityConfig:
    max_cells: int
    continue_on_cell_error: bool
    run_backtest: bool
    include_benchmark: bool
    include_monte_carlo: bool
    include_walk_forward: bool
    primary_metric: SensitivityMetricName
    stability_metric: SensitivityMetricName
    min_completed_cells: int

@dataclass
class SensitivityCellResult:
    cell: ParameterGridCell
    status: SensitivityCellStatus
    backtest_run_id: str | None
    metrics: dict[str, Any]
    benchmark_summary: dict[str, Any] = field(default_factory=dict)
    robustness_summary: dict[str, Any] = field(default_factory=dict)
    walk_forward_summary: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class ParameterSensitivityRunResult:
    run_id: str
    created_at_utc: str
    status: SensitivityRunStatus
    strategy_name: str
    grid_spec: ParameterGridSpec
    config: ParameterSensitivityConfig
    cells: list[ParameterGridCell]
    cell_results: list[SensitivityCellResult]
    aggregate_metrics: dict[str, Any]
    stability_bucket: StabilityBucket
    overfit_risk_hint: OverfitRiskHint
    robust_regions: list[dict[str, Any]]
    fragile_regions: list[dict[str, Any]]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def parameter_range_spec_to_dict(spec: ParameterRangeSpec) -> dict:
    return {
        "name": spec.name,
        "value_type": spec.value_type.value,
        "values": spec.values,
        "default_value": spec.default_value,
        "description": spec.description
    }

def parameter_grid_spec_to_dict(spec: ParameterGridSpec) -> dict:
    return {
        "grid_id": spec.grid_id,
        "strategy_name": spec.strategy_name,
        "grid_type": spec.grid_type.value,
        "parameters": [parameter_range_spec_to_dict(p) for p in spec.parameters],
        "max_cells": spec.max_cells,
        "metadata": spec.metadata
    }

def parameter_grid_cell_to_dict(cell: ParameterGridCell) -> dict:
    return {
        "cell_id": cell.cell_id,
        "index": cell.index,
        "strategy_name": cell.strategy_name,
        "params": cell.params,
        "status": cell.status.value,
        "metadata": cell.metadata
    }

def sensitivity_cell_result_to_dict(result: SensitivityCellResult) -> dict:
    return {
        "cell": parameter_grid_cell_to_dict(result.cell),
        "status": result.status.value,
        "backtest_run_id": result.backtest_run_id,
        "metrics": result.metrics,
        "benchmark_summary": result.benchmark_summary,
        "robustness_summary": result.robustness_summary,
        "walk_forward_summary": result.walk_forward_summary,
        "warnings": result.warnings,
        "errors": result.errors
    }

def parameter_sensitivity_run_result_to_dict(result: ParameterSensitivityRunResult) -> dict:
    return {
        "run_id": result.run_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "strategy_name": result.strategy_name,
        "grid_spec": parameter_grid_spec_to_dict(result.grid_spec),
        "config": {
            "max_cells": result.config.max_cells,
            "continue_on_cell_error": result.config.continue_on_cell_error,
            "run_backtest": result.config.run_backtest,
            "include_benchmark": result.config.include_benchmark,
            "include_monte_carlo": result.config.include_monte_carlo,
            "include_walk_forward": result.config.include_walk_forward,
            "primary_metric": result.config.primary_metric.value,
            "stability_metric": result.config.stability_metric.value,
            "min_completed_cells": result.config.min_completed_cells
        },
        "cells": [parameter_grid_cell_to_dict(c) for c in result.cells],
        "cell_results": [sensitivity_cell_result_to_dict(r) for r in result.cell_results],
        "aggregate_metrics": result.aggregate_metrics,
        "stability_bucket": result.stability_bucket.value,
        "overfit_risk_hint": result.overfit_risk_hint.value,
        "robust_regions": result.robust_regions,
        "fragile_regions": result.fragile_regions,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

def validate_parameter_range_spec(spec: ParameterRangeSpec) -> None:
    from usa_signal_bot.core.exceptions import ParameterGridError
    if not spec.name:
        raise ParameterGridError("ParameterRangeSpec name cannot be empty")
    if not spec.values:
        raise ParameterGridError(f"ParameterRangeSpec values cannot be empty for param: {spec.name}")
    if not isinstance(spec.value_type, ParameterValueType):
        raise ParameterGridError(f"Invalid value_type for param {spec.name}")

    for val in spec.values:
        if spec.value_type == ParameterValueType.INT and not isinstance(val, int):
            raise ParameterGridError(f"Value {val} must be int for param {spec.name}")
        if spec.value_type == ParameterValueType.FLOAT and not isinstance(val, (float, int)):
            raise ParameterGridError(f"Value {val} must be float for param {spec.name}")
        if spec.value_type == ParameterValueType.BOOL and not isinstance(val, bool):
            raise ParameterGridError(f"Value {val} must be bool for param {spec.name}")
        if spec.value_type == ParameterValueType.STR and not isinstance(val, str):
            raise ParameterGridError(f"Value {val} must be str for param {spec.name}")

    if spec.default_value is not None:
        if spec.default_value not in spec.values:
            pass # In practice, a default value might be from schema and not in the grid, which is okay. But tip type validation should ideally pass.

def validate_parameter_grid_spec(spec: ParameterGridSpec) -> None:
    from usa_signal_bot.core.exceptions import ParameterGridError
    if not spec.grid_id:
        raise ParameterGridError("ParameterGridSpec grid_id cannot be empty")
    if not spec.strategy_name:
        raise ParameterGridError("ParameterGridSpec strategy_name cannot be empty")
    if not spec.parameters:
        raise ParameterGridError("ParameterGridSpec parameters cannot be empty")
    if spec.max_cells <= 0:
        raise ParameterGridError(f"max_cells must be positive, got: {spec.max_cells}")
    for p in spec.parameters:
        validate_parameter_range_spec(p)

def validate_parameter_sensitivity_config(config: ParameterSensitivityConfig) -> None:
    from usa_signal_bot.core.exceptions import ParameterSensitivityError
    if config.max_cells <= 0:
        raise ParameterSensitivityError("max_cells must be positive")
    if config.min_completed_cells <= 0:
        raise ParameterSensitivityError("min_completed_cells must be positive")

def create_sensitivity_run_id(strategy_name: str) -> str:
    return f"sens_{strategy_name}_{uuid.uuid4().hex[:8]}"
