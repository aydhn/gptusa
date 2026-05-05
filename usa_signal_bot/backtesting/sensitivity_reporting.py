import json
from pathlib import Path
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterGridSpec, SensitivityCellResult, ParameterSensitivityRunResult,
    parameter_sensitivity_run_result_to_dict
)
from usa_signal_bot.backtesting.stability_map import StabilityMap
from usa_signal_bot.backtesting.sensitivity_validation import SensitivityValidationReport

def parameter_grid_spec_to_text(spec: ParameterGridSpec) -> str:
    lines = [
        f"Parameter Grid Spec (ID: {spec.grid_id})",
        f"Strategy: {spec.strategy_name}",
        f"Type: {spec.grid_type.value}",
        f"Max Cells: {spec.max_cells}",
        "Parameters:"
    ]
    for p in spec.parameters:
        lines.append(f"  - {p.name} ({p.value_type.value}): {p.values}")
    return "\n".join(lines)

def sensitivity_cell_result_to_text(result: SensitivityCellResult) -> str:
    lines = [
        f"Cell: {result.cell.cell_id} | Index: {result.cell.index}",
        f"Params: {result.cell.params}",
        f"Status: {result.status.value}",
        f"Metrics: {result.metrics}"
    ]
    return "\n".join(lines)

def parameter_sensitivity_run_result_to_text(result: ParameterSensitivityRunResult, limit: int = 30) -> str:
    lines = [
        "========================================",
        "PARAMETER SENSITIVITY RUN RESULT",
        "========================================",
        f"Run ID: {result.run_id}",
        f"Created: {result.created_at_utc}",
        f"Status: {result.status.value}",
        f"Strategy: {result.strategy_name}",
        "",
        parameter_grid_spec_to_text(result.grid_spec),
        "",
        "--- Aggregate Metrics ---"
    ]
    for k, v in result.aggregate_metrics.items():
        lines.append(f"  {k}: {v}")

    lines.extend([
        "",
        f"Stability Bucket: {result.stability_bucket.value}",
        f"Overfit Risk Hint: {result.overfit_risk_hint.value}",
        f"Robust Regions Found: {len(result.robust_regions)}",
        f"Fragile Regions Found: {len(result.fragile_regions)}",
        "",
        f"--- Cell Results (Limit: {limit}) ---"
    ])

    for i, c_res in enumerate(result.cell_results):
        if i >= limit:
            lines.append(f"... and {len(result.cell_results) - limit} more cells")
            break
        lines.append(f"  {c_res.cell.cell_id} | {c_res.status.value} | {c_res.metrics}")

    return "\n".join(lines)

def sensitivity_summary_to_text(result: ParameterSensitivityRunResult) -> str:
    lines = [
        f"Run ID: {result.run_id}",
        f"Strategy: {result.strategy_name}",
        f"Status: {result.status.value}",
        f"Stability: {result.stability_bucket.value}",
        f"Overfit Risk: {result.overfit_risk_hint.value}"
    ]
    return " | ".join(lines)

def stability_map_report_to_text(map_: StabilityMap, limit: int = 30) -> str:
    from usa_signal_bot.backtesting.stability_map import stability_map_to_text
    return stability_map_to_text(map_, limit)

def sensitivity_limitations_text() -> str:
    return """
LIMITATIONS AND WARNINGS:
- This tool does NOT perform optimization and does NOT select 'best parameters'.
- Results represent historical sensitivity and do NOT guarantee future performance.
- Stability maps identify robust neighborhoods but are subject to survivorship bias and data quality.
- Do NOT use these results as direct investment advice or live trading confirmation.
"""

def write_sensitivity_report_json(path: Path, result: ParameterSensitivityRunResult, validation_report: SensitivityValidationReport | None = None) -> Path:
    data = {
        "result": parameter_sensitivity_run_result_to_dict(result),
        "limitations": sensitivity_limitations_text()
    }
    if validation_report:
        data["validation_report"] = {
            "valid": validation_report.valid,
            "errors": validation_report.errors
        }

    temp_path = path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    temp_path.replace(path)
    return path
