import statistics
from dataclasses import dataclass, field
from typing import Any
from usa_signal_bot.core.enums import SensitivityMetricName, ParameterZoneType, StabilityBucket
from usa_signal_bot.backtesting.parameter_sensitivity_models import SensitivityCellResult, SensitivityCellStatus
from usa_signal_bot.backtesting.sensitivity_metrics import extract_cell_metric, calculate_stability_score_from_values

@dataclass
class StabilityMapCell:
    cell_id: str
    params: dict[str, Any]
    primary_metric_value: float | None
    stability_score: float | None
    zone_type: ParameterZoneType
    neighbors: list[str]
    warnings: list[str]

@dataclass
class StabilityMap:
    map_id: str
    strategy_name: str
    primary_metric: SensitivityMetricName
    cells: list[StabilityMapCell]
    robust_regions: list[dict[str, Any]]
    fragile_regions: list[dict[str, Any]]
    stability_bucket: StabilityBucket
    warnings: list[str]
    errors: list[str]

def find_neighbor_cells(cell: SensitivityCellResult, all_results: list[SensitivityCellResult]) -> list[str]:
    neighbors = []
    # Simplified neighbor detection: any cell with 1 parameter difference is a neighbor
    for other in all_results:
        if other.cell.cell_id == cell.cell.cell_id or other.status != SensitivityCellStatus.COMPLETED:
            continue

        diff_count = 0
        for k, v in cell.cell.params.items():
            if k not in other.cell.params or other.cell.params[k] != v:
                diff_count += 1

        if diff_count <= 1:
            neighbors.append(other.cell.cell_id)

    return neighbors

def calculate_local_stability_score(cell: SensitivityCellResult, neighbors: list[SensitivityCellResult], primary_metric: SensitivityMetricName) -> float | None:
    vals = []
    cell_val = extract_cell_metric(cell, primary_metric)
    if cell_val is not None:
        vals.append(cell_val)

    for n in neighbors:
        n_val = extract_cell_metric(n, primary_metric)
        if n_val is not None:
            vals.append(n_val)

    return calculate_stability_score_from_values(vals)

def classify_parameter_zone(cell_value: float | None, local_stability: float | None, global_median: float | None) -> ParameterZoneType:
    if cell_value is None or local_stability is None or global_median is None:
        return ParameterZoneType.INSUFFICIENT_DATA

    if cell_value >= global_median and local_stability >= 60:
        return ParameterZoneType.ROBUST_REGION

    if cell_value >= global_median and local_stability < 40:
        return ParameterZoneType.FRAGILE_REGION

    if cell_value > global_median * 3 and local_stability < 20:
        return ParameterZoneType.OUTLIER_REGION

    return ParameterZoneType.NEUTRAL_REGION

def detect_robust_regions(map_: StabilityMap, min_region_size: int = 2) -> list[dict[str, Any]]:
    # In a full implementation, this would do clustering. For now, we group by robust cells
    robust_cells = [c for c in map_.cells if c.zone_type == ParameterZoneType.ROBUST_REGION]
    if len(robust_cells) >= min_region_size:
        return [{"region_name": "primary_robust_zone", "cells": [c.cell_id for c in robust_cells]}]
    return []

def detect_fragile_regions(map_: StabilityMap, min_region_size: int = 1) -> list[dict[str, Any]]:
    fragile_cells = [c for c in map_.cells if c.zone_type == ParameterZoneType.FRAGILE_REGION]
    if len(fragile_cells) >= min_region_size:
        return [{"region_name": "primary_fragile_zone", "cells": [c.cell_id for c in fragile_cells]}]
    return []

def build_stability_map(results: list[SensitivityCellResult], primary_metric: SensitivityMetricName) -> StabilityMap:
    from usa_signal_bot.backtesting.sensitivity_metrics import calculate_stability_score_from_values

    all_vals = [extract_cell_metric(r, primary_metric) for r in results if r.status == SensitivityCellStatus.COMPLETED]
    all_vals = [v for v in all_vals if v is not None]

    global_median = statistics.median(all_vals) if all_vals else None

    map_cells = []
    for r in results:
        if r.status != SensitivityCellStatus.COMPLETED:
            continue

        neighbor_ids = find_neighbor_cells(r, results)
        neighbor_results = [nr for nr in results if nr.cell.cell_id in neighbor_ids and nr.status == SensitivityCellStatus.COMPLETED]

        local_stab = calculate_local_stability_score(r, neighbor_results, primary_metric)
        cell_val = extract_cell_metric(r, primary_metric)

        zone = classify_parameter_zone(cell_val, local_stab, global_median)

        map_cells.append(StabilityMapCell(
            cell_id=r.cell.cell_id,
            params=r.cell.params,
            primary_metric_value=cell_val,
            stability_score=local_stab,
            zone_type=zone,
            neighbors=neighbor_ids,
            warnings=[]
        ))

    smap = StabilityMap(
        map_id="map_1",
        strategy_name=results[0].cell.strategy_name if results else "unknown",
        primary_metric=primary_metric,
        cells=map_cells,
        robust_regions=[],
        fragile_regions=[],
        stability_bucket=StabilityBucket.UNKNOWN,
        warnings=[],
        errors=[]
    )

    smap.robust_regions = detect_robust_regions(smap)
    smap.fragile_regions = detect_fragile_regions(smap)
    return smap

def stability_map_to_dict(map_: StabilityMap) -> dict:
    return {
        "map_id": map_.map_id,
        "strategy_name": map_.strategy_name,
        "primary_metric": map_.primary_metric.value,
        "cells": [
            {
                "cell_id": c.cell_id,
                "params": c.params,
                "primary_metric_value": c.primary_metric_value,
                "stability_score": c.stability_score,
                "zone_type": c.zone_type.value,
                "neighbors": c.neighbors
            } for c in map_.cells
        ],
        "robust_regions": map_.robust_regions,
        "fragile_regions": map_.fragile_regions,
        "stability_bucket": map_.stability_bucket.value,
        "warnings": map_.warnings,
        "errors": map_.errors
    }

def stability_map_to_text(map_: StabilityMap, limit: int = 30) -> str:
    lines = [f"Stability Map: {map_.strategy_name} ({len(map_.cells)} cells)"]
    for i, c in enumerate(map_.cells):
        if i >= limit:
            lines.append("...")
            break
        lines.append(f"  {c.cell_id} | {c.zone_type.value} | Stab: {c.stability_score} | Val: {c.primary_metric_value}")
    return "\n".join(lines)
