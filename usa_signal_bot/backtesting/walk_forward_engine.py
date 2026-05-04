from pathlib import Path
from datetime import datetime, timezone
import logging

from usa_signal_bot.core.enums import (
    WalkForwardRunStatus,
    WalkForwardWindowStatus,
    WalkForwardMode,
    BacktestRunStatus
)
from usa_signal_bot.core.exceptions import WalkForwardEngineError
from usa_signal_bot.backtesting.walk_forward_models import (
    WalkForwardRunRequest,
    WalkForwardRunResult,
    WalkForwardWindow,
    WalkForwardWindowResult,
    create_walk_forward_run_id
)
from usa_signal_bot.backtesting.walk_forward_windows import (
    generate_walk_forward_windows,
    infer_date_range_from_cached_bars
)
from usa_signal_bot.backtesting.walk_forward_metrics import (
    calculate_walk_forward_aggregate_metrics,
    classify_walk_forward_stability,
    classify_out_of_sample_result,
    walk_forward_aggregate_metrics_to_dict
)
from usa_signal_bot.backtesting.walk_forward_store import (
    build_walk_forward_run_dir,
    write_walk_forward_result_json,
    write_walk_forward_windows_json,
    write_walk_forward_window_results_jsonl,
    write_walk_forward_aggregate_metrics_json
)
from usa_signal_bot.backtesting.backtest_engine import BacktestEngine, BacktestRunRequest

logger = logging.getLogger(__name__)

class WalkForwardEngine:
    def __init__(self, data_root: Path, backtest_engine: BacktestEngine | None = None):
        self.data_root = data_root
        self.backtest_engine = backtest_engine or BacktestEngine(data_root)

    def run(self, request: WalkForwardRunRequest) -> WalkForwardRunResult:
        run_id = create_walk_forward_run_id(request.run_name)
        created_at_utc = datetime.now(timezone.utc).isoformat()

        warnings = []
        errors = []

        start_dt = request.start_date
        end_dt = request.end_date

        if not start_dt or not end_dt:
            infer_start, infer_end, infer_warns = infer_date_range_from_cached_bars(
                self.data_root, request.symbols, request.timeframe
            )
            warnings.extend(infer_warns)

            if not start_dt:
                start_dt = infer_start
            if not end_dt:
                end_dt = infer_end

        if not start_dt or not end_dt:
            errors.append("Could not infer date range from cache. Explicit dates required.")
            return self._build_failed_result(run_id, request, created_at_utc, warnings, errors)

        try:
            windows = generate_walk_forward_windows(start_dt, end_dt, request.config)
        except Exception as e:
            errors.append(f"Failed to generate windows: {e}")
            return self._build_failed_result(run_id, request, created_at_utc, warnings, errors)

        if not windows:
            errors.append("No windows generated for the given date range and config.")
            return self._build_failed_result(run_id, request, created_at_utc, warnings, errors)

        window_results = []

        for w in windows:
            w.status = WalkForwardWindowStatus.RUNNING
            try:
                w_res = self.run_window(run_id, w, request)
                if w_res.errors:
                    w.status = WalkForwardWindowStatus.PARTIAL_SUCCESS if w_res.in_sample_result_id or w_res.out_of_sample_result_id else WalkForwardWindowStatus.FAILED
                else:
                    w.status = WalkForwardWindowStatus.COMPLETED
                window_results.append(w_res)
            except Exception as e:
                logger.error(f"Window {w.window_id} failed completely: {e}")
                w.status = WalkForwardWindowStatus.FAILED
                window_results.append(WalkForwardWindowResult(
                    window=w,
                    in_sample_result_id=None,
                    out_of_sample_result_id=None,
                    in_sample_metrics={},
                    out_of_sample_metrics={},
                    errors=[str(e)]
                ))
                # Depending on config, we might want to continue or break.
                # Default is continue_on_window_error = true

        agg_metrics_obj = calculate_walk_forward_aggregate_metrics(window_results)
        agg_metrics = walk_forward_aggregate_metrics_to_dict(agg_metrics_obj)

        stability_bucket = classify_walk_forward_stability(agg_metrics_obj.stability_score)
        oos_bucket = classify_out_of_sample_result(agg_metrics_obj)

        status = WalkForwardRunStatus.COMPLETED
        if any(w.status == WalkForwardWindowStatus.FAILED for w in windows):
             status = WalkForwardRunStatus.PARTIAL_SUCCESS
        if all(w.status == WalkForwardWindowStatus.FAILED for w in windows):
             status = WalkForwardRunStatus.FAILED

        res = WalkForwardRunResult(
            run_id=run_id,
            run_name=request.run_name,
            status=status,
            request=request,
            windows=windows,
            window_results=window_results,
            aggregate_metrics=agg_metrics,
            stability_bucket=stability_bucket,
            oos_bucket=oos_bucket,
            output_paths={},
            warnings=warnings,
            errors=errors,
            created_at_utc=created_at_utc
        )

        return res

    def _build_failed_result(self, run_id, request, created_at_utc, warnings, errors):
        return WalkForwardRunResult(
            run_id=run_id,
            run_name=request.run_name,
            status=WalkForwardRunStatus.FAILED,
            request=request,
            windows=[],
            window_results=[],
            aggregate_metrics={},
            stability_bucket="UNKNOWN",
            oos_bucket="UNKNOWN",
            output_paths={},
            warnings=warnings,
            errors=errors,
            created_at_utc=created_at_utc
        )

    def run_window(self, run_id: str, window: WalkForwardWindow, request: WalkForwardRunRequest) -> WalkForwardWindowResult:
        is_req = self.build_in_sample_backtest_request(run_id, window, request)
        oos_req = self.build_out_of_sample_backtest_request(run_id, window, request)

        is_res = self.backtest_engine.run(is_req)
        is_metrics = is_res.metrics if is_res.status in (BacktestRunStatus.COMPLETED, BacktestRunStatus.PARTIAL_SUCCESS) else {}
        is_id = is_res.run_id if is_res.status in (BacktestRunStatus.COMPLETED, BacktestRunStatus.PARTIAL_SUCCESS) else None

        oos_res = self.backtest_engine.run(oos_req)
        oos_metrics = oos_res.metrics if oos_res.status in (BacktestRunStatus.COMPLETED, BacktestRunStatus.PARTIAL_SUCCESS) else {}
        oos_id = oos_res.run_id if oos_res.status in (BacktestRunStatus.COMPLETED, BacktestRunStatus.PARTIAL_SUCCESS) else None

        # Note: Benchmark and attribution can be added here if enabled in config

        warns = is_res.warnings + oos_res.warnings
        errs = is_res.errors + oos_res.errors

        return WalkForwardWindowResult(
            window=window,
            in_sample_result_id=is_id,
            out_of_sample_result_id=oos_id,
            in_sample_metrics=is_metrics,
            out_of_sample_metrics=oos_metrics,
            warnings=warns,
            errors=errs
        )

    def build_in_sample_backtest_request(self, wf_run_id: str, window: WalkForwardWindow, request: WalkForwardRunRequest) -> BacktestRunRequest:
        from usa_signal_bot.backtesting.backtest_engine import BacktestRunConfig

        # Fallback to default if not provided
        bc_dict = request.backtest_config or {}

        # Reconstruct BacktestRunConfig
        bc = BacktestRunConfig(
            starting_cash=bc_dict.get("starting_cash", 100000.0),
            fee_rate=bc_dict.get("fee_rate", 0.0),
            slippage_bps=bc_dict.get("slippage_bps", 0.0),
            signal_to_order=bc_dict.get("signal_to_order", "MARKET_NEXT_OPEN"),
            exit_mode=bc_dict.get("exit_mode", "HOLD_N_BARS"),
            hold_bars=bc_dict.get("hold_bars", 5),
            max_positions=bc_dict.get("max_positions", 10),
            max_position_notional=bc_dict.get("max_position_notional", 10000.0),
            allow_fractional_quantity=bc_dict.get("allow_fractional_quantity", True)
        )

        return BacktestRunRequest(
            run_name=f"{wf_run_id}_win_{window.index:03d}_is",
            symbols=request.symbols,
            timeframe=request.timeframe,
            provider_name="yfinance",
            signal_file=request.signal_file,
            selected_candidates_file=request.selected_candidates_file,
            start_date=window.train_start,
            end_date=window.train_end,
            config=bc
        )

    def build_out_of_sample_backtest_request(self, wf_run_id: str, window: WalkForwardWindow, request: WalkForwardRunRequest) -> BacktestRunRequest:
        from usa_signal_bot.backtesting.backtest_engine import BacktestRunConfig

        bc_dict = request.backtest_config or {}

        bc = BacktestRunConfig(
            starting_cash=bc_dict.get("starting_cash", 100000.0),
            fee_rate=bc_dict.get("fee_rate", 0.0),
            slippage_bps=bc_dict.get("slippage_bps", 0.0),
            signal_to_order=bc_dict.get("signal_to_order", "MARKET_NEXT_OPEN"),
            exit_mode=bc_dict.get("exit_mode", "HOLD_N_BARS"),
            hold_bars=bc_dict.get("hold_bars", 5),
            max_positions=bc_dict.get("max_positions", 10),
            max_position_notional=bc_dict.get("max_position_notional", 10000.0),
            allow_fractional_quantity=bc_dict.get("allow_fractional_quantity", True)
        )

        return BacktestRunRequest(
            run_name=f"{wf_run_id}_win_{window.index:03d}_oos",
            symbols=request.symbols,
            timeframe=request.timeframe,
            provider_name="yfinance",
            signal_file=request.signal_file,
            selected_candidates_file=request.selected_candidates_file,
            start_date=window.test_start,
            end_date=window.test_end,
            config=bc
        )

    def write_result(self, result: WalkForwardRunResult) -> list[Path]:
        run_dir = build_walk_forward_run_dir(self.data_root, result.run_id)
        paths = []
        paths.append(write_walk_forward_result_json(run_dir / "result.json", result))
        paths.append(write_walk_forward_windows_json(run_dir / "windows.json", result.windows))
        paths.append(write_walk_forward_window_results_jsonl(run_dir / "window_results.jsonl", result.window_results))

        from usa_signal_bot.backtesting.walk_forward_metrics import WalkForwardAggregateMetrics
        if result.aggregate_metrics:
             # Just map dict back to object or skip strong typing here since it's just saving dict
             import json
             p = run_dir / "aggregate_metrics.json"
             with open(p, "w") as f:
                 json.dump(result.aggregate_metrics, f, indent=2, default=str)
             paths.append(p)

        from usa_signal_bot.backtesting.walk_forward_reporting import write_walk_forward_report_json
        paths.append(write_walk_forward_report_json(run_dir / "report.json", result))

        result.output_paths = {p.name: str(p) for p in paths}

        # update result one more time to include output paths
        write_walk_forward_result_json(run_dir / "result.json", result)

        return paths
