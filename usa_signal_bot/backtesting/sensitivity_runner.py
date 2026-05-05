from dataclasses import replace
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.core.enums import SensitivityRunStatus, SensitivityCellStatus, StabilityBucket, OverfitRiskHint
from usa_signal_bot.backtesting.backtest_engine import BacktestEngine, BacktestRunRequest, BacktestRunResult, BacktestRunStatus
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterGridSpec, ParameterSensitivityConfig, ParameterGridCell,
    SensitivityCellResult, ParameterSensitivityRunResult, create_sensitivity_run_id
)
from usa_signal_bot.backtesting.parameter_grid import create_parameter_grid_cells
from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
import usa_signal_bot.backtesting.sensitivity_metrics as sensitivity_metrics
import usa_signal_bot.backtesting.stability_map as stability_map
import usa_signal_bot.backtesting.sensitivity_store as sensitivity_store

class ParameterSensitivityRunner:
    def __init__(self, data_root: Path, backtest_engine: BacktestEngine | None = None, strategy_registry: StrategyRegistry | None = None):
        self.data_root = data_root
        self.backtest_engine = backtest_engine or BacktestEngine(data_root)
        self.strategy_registry = strategy_registry or StrategyRegistry()

    def build_backtest_request_for_cell(self, base_request: BacktestRunRequest, cell: ParameterGridCell) -> BacktestRunRequest:
        # In this phase, we attach the strategy params via config metadata for tracking,
        # as signal generation with direct strategy param passing is for later phases.

        # Determine the name
        run_name = f"{base_request.run_name}_{cell.cell_id}"

        # Clone base config if present, or create empty, and add params
        config = base_request.config

        # We don't have a direct backtest_engine metadata field in BacktestRunRequest usually,
        # but we assume the runner just passes this as a logical run.
        return replace(base_request, run_name=run_name)

    def collect_cell_metrics(self, backtest_result: BacktestRunResult) -> dict[str, Any]:
        metrics_dict = {}
        if backtest_result.metrics:
            metrics_dict["total_return_pct"] = backtest_result.metrics.total_return_pct
            metrics_dict["max_drawdown_pct"] = backtest_result.metrics.max_drawdown_pct
            metrics_dict["win_rate"] = backtest_result.metrics.win_rate
            metrics_dict["profit_factor"] = backtest_result.metrics.profit_factor
            metrics_dict["sharpe_ratio"] = backtest_result.metrics.sharpe_ratio
        return metrics_dict

    def run_cell(self, base_request: BacktestRunRequest, cell: ParameterGridCell, config: ParameterSensitivityConfig) -> SensitivityCellResult:
        cell_request = self.build_backtest_request_for_cell(base_request, cell)
        try:
            if config.run_backtest:
                backtest_result = self.backtest_engine.run(cell_request)
                if backtest_result.status == BacktestRunStatus.COMPLETED:
                    metrics = self.collect_cell_metrics(backtest_result)
                    return SensitivityCellResult(
                        cell=cell,
                        status=SensitivityCellStatus.COMPLETED,
                        backtest_run_id=backtest_result.run_id,
                        metrics=metrics,
                        warnings=backtest_result.warnings,
                        errors=backtest_result.errors
                    )
                else:
                    return SensitivityCellResult(
                        cell=cell,
                        status=SensitivityCellStatus.FAILED,
                        backtest_run_id=backtest_result.run_id,
                        metrics={},
                        errors=[f"Backtest failed with status: {backtest_result.status}"]
                    )
            else:
                return SensitivityCellResult(
                    cell=cell,
                    status=SensitivityCellStatus.SKIPPED,
                    backtest_run_id=None,
                    metrics={},
                    warnings=["run_backtest is False. Cell skipped."]
                )
        except Exception as e:
            return SensitivityCellResult(
                cell=cell,
                status=SensitivityCellStatus.FAILED,
                backtest_run_id=None,
                metrics={},
                errors=[f"Cell exception: {str(e)}"]
            )

    def run(self, request: BacktestRunRequest, grid_spec: ParameterGridSpec, config: ParameterSensitivityConfig | None = None) -> ParameterSensitivityRunResult:
        if not config:
            raise ValueError("ParameterSensitivityConfig must be provided")

        run_id = create_sensitivity_run_id(grid_spec.strategy_name)
        created_at_utc = datetime.now(timezone.utc).isoformat()

        cells = create_parameter_grid_cells(grid_spec)
        cell_results = []
        warnings = []
        errors = []

        for cell in cells:
            cell_result = self.run_cell(request, cell, config)
            cell_results.append(cell_result)

            if cell_result.status == SensitivityCellStatus.FAILED and not config.continue_on_cell_error:
                errors.append(f"Cell {cell.cell_id} failed and continue_on_cell_error is False. Halting.")
                break

        completed_count = sum(1 for r in cell_results if r.status == SensitivityCellStatus.COMPLETED)

        if completed_count == 0:
            status = SensitivityRunStatus.FAILED
            errors.append("No cells completed successfully.")
        elif completed_count < len(cells):
            status = SensitivityRunStatus.PARTIAL_SUCCESS
            if completed_count < config.min_completed_cells:
                warnings.append(f"Only {completed_count} cells completed, below min_completed_cells={config.min_completed_cells}")
        else:
            status = SensitivityRunStatus.COMPLETED

        aggregate_metrics = {}
        stability_bucket = StabilityBucket.UNKNOWN
        overfit_risk_hint = OverfitRiskHint.UNKNOWN
        robust_regions = []
        fragile_regions = []

        if completed_count > 0:
            agg_metrics_obj = sensitivity_metrics.calculate_sensitivity_aggregate_metrics(cell_results, config.primary_metric)
            aggregate_metrics = sensitivity_metrics.sensitivity_aggregate_metrics_to_dict(agg_metrics_obj)
            stability_bucket = agg_metrics_obj.stability_bucket if hasattr(agg_metrics_obj, 'stability_bucket') else sensitivity_metrics.classify_stability_bucket(agg_metrics_obj.stability_score, completed_count)
            overfit_risk_hint = sensitivity_metrics.classify_overfit_risk_hint(agg_metrics_obj)

            smap = stability_map.build_stability_map(cell_results, config.primary_metric)
            robust_regions = smap.robust_regions
            fragile_regions = smap.fragile_regions

        return ParameterSensitivityRunResult(
            run_id=run_id,
            created_at_utc=created_at_utc,
            status=status,
            strategy_name=grid_spec.strategy_name,
            grid_spec=grid_spec,
            config=config,
            cells=cells,
            cell_results=cell_results,
            aggregate_metrics=aggregate_metrics,
            stability_bucket=stability_bucket,
            overfit_risk_hint=overfit_risk_hint,
            robust_regions=robust_regions,
            fragile_regions=fragile_regions,
            output_paths={},
            warnings=warnings,
            errors=errors
        )

    def write_result(self, result: ParameterSensitivityRunResult) -> list[Path]:
        return []
