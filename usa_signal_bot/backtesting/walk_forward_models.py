from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import (
    WalkForwardMode,
    WalkForwardWindowStatus,
    WalkForwardRunStatus,
    WalkForwardStabilityBucket,
    OutOfSampleResultBucket
)

@dataclass
class WalkForwardWindow:
    window_id: str
    index: int
    mode: WalkForwardMode
    train_start: str
    train_end: str
    test_start: str
    test_end: str
    full_start: str
    full_end: str
    status: WalkForwardWindowStatus = WalkForwardWindowStatus.CREATED
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class WalkForwardConfig:
    mode: WalkForwardMode
    train_window_days: int
    test_window_days: int
    step_days: int
    min_train_days: int
    max_windows: int
    anchored_start: bool
    include_partial_last_window: bool

@dataclass
class WalkForwardWindowResult:
    window: WalkForwardWindow
    in_sample_result_id: str | None
    out_of_sample_result_id: str | None
    in_sample_metrics: dict[str, Any]
    out_of_sample_metrics: dict[str, Any]
    benchmark_summary: dict[str, Any] = field(default_factory=dict)
    attribution_summary: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class WalkForwardRunRequest:
    run_name: str
    symbols: list[str]
    timeframe: str
    signal_file: str | None = None
    selected_candidates_file: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    config: WalkForwardConfig | None = None
    backtest_config: dict[str, Any] = field(default_factory=dict)
    enable_benchmark_comparison: bool = False
    benchmark_set_name: str = "default"

@dataclass
class WalkForwardRunResult:
    run_id: str
    run_name: str
    status: WalkForwardRunStatus
    request: WalkForwardRunRequest
    windows: list[WalkForwardWindow]
    window_results: list[WalkForwardWindowResult]
    aggregate_metrics: dict[str, Any]
    stability_bucket: WalkForwardStabilityBucket
    oos_bucket: OutOfSampleResultBucket
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]
    created_at_utc: str

def validate_walk_forward_window(window: WalkForwardWindow) -> None:
    from usa_signal_bot.core.exceptions import WalkForwardWindowError
    if not window.window_id:
        raise WalkForwardWindowError("window_id cannot be empty")
    if window.index < 0:
        raise WalkForwardWindowError("index cannot be negative")
    for date_field in ["train_start", "train_end", "test_start", "test_end", "full_start", "full_end"]:
        if not getattr(window, date_field):
            raise WalkForwardWindowError(f"{date_field} cannot be empty")

    if not (window.train_start <= window.train_end <= window.test_start <= window.test_end):
        raise WalkForwardWindowError(f"Invalid date sequence: train_start {window.train_start} <= train_end {window.train_end} < test_start {window.test_start} <= test_end {window.test_end}")

    if not window.full_start <= window.train_start:
         raise WalkForwardWindowError("full_start must be <= train_start")
    if not window.test_end <= window.full_end:
         raise WalkForwardWindowError("test_end must be <= full_end")


def validate_walk_forward_config(config: WalkForwardConfig) -> None:
    from usa_signal_bot.core.exceptions import WalkForwardError
    if config.train_window_days <= 0:
        raise WalkForwardError("train_window_days must be positive")
    if config.test_window_days <= 0:
        raise WalkForwardError("test_window_days must be positive")
    if config.step_days <= 0:
        raise WalkForwardError("step_days must be positive")
    if config.max_windows <= 0:
        raise WalkForwardError("max_windows must be positive")
    if config.min_train_days <= 0:
        raise WalkForwardError("min_train_days must be positive")

    if not isinstance(config.mode, WalkForwardMode):
        try:
             WalkForwardMode(config.mode)
        except ValueError:
            raise WalkForwardError(f"Invalid walk forward mode: {config.mode}")

def create_walk_forward_run_id(run_name: str) -> str:
    from datetime import datetime, timezone
    safe_name = "".join(c if c.isalnum() else "_" for c in run_name)
    now_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    short_uuid = str(uuid.uuid4())[:8]
    return f"wf_{safe_name}_{now_str}_{short_uuid}"

def walk_forward_window_to_dict(window: WalkForwardWindow) -> dict:
    return {
        "window_id": window.window_id,
        "index": window.index,
        "mode": window.mode.value if isinstance(window.mode, WalkForwardMode) else window.mode,
        "train_start": window.train_start,
        "train_end": window.train_end,
        "test_start": window.test_start,
        "test_end": window.test_end,
        "full_start": window.full_start,
        "full_end": window.full_end,
        "status": window.status.value if isinstance(window.status, WalkForwardWindowStatus) else window.status,
        "metadata": window.metadata
    }

def walk_forward_config_to_dict(config: WalkForwardConfig) -> dict:
    return {
        "mode": config.mode.value if isinstance(config.mode, WalkForwardMode) else config.mode,
        "train_window_days": config.train_window_days,
        "test_window_days": config.test_window_days,
        "step_days": config.step_days,
        "min_train_days": config.min_train_days,
        "max_windows": config.max_windows,
        "anchored_start": config.anchored_start,
        "include_partial_last_window": config.include_partial_last_window
    }

def walk_forward_window_result_to_dict(result: WalkForwardWindowResult) -> dict:
    return {
        "window": walk_forward_window_to_dict(result.window),
        "in_sample_result_id": result.in_sample_result_id,
        "out_of_sample_result_id": result.out_of_sample_result_id,
        "in_sample_metrics": result.in_sample_metrics,
        "out_of_sample_metrics": result.out_of_sample_metrics,
        "benchmark_summary": result.benchmark_summary,
        "attribution_summary": result.attribution_summary,
        "warnings": result.warnings,
        "errors": result.errors
    }

def walk_forward_run_request_to_dict(request: WalkForwardRunRequest) -> dict:
    return {
        "run_name": request.run_name,
        "symbols": request.symbols,
        "timeframe": request.timeframe,
        "signal_file": request.signal_file,
        "selected_candidates_file": request.selected_candidates_file,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "config": walk_forward_config_to_dict(request.config) if request.config else None,
        "backtest_config": request.backtest_config,
        "enable_benchmark_comparison": request.enable_benchmark_comparison,
        "benchmark_set_name": request.benchmark_set_name
    }

def walk_forward_run_result_to_dict(result: WalkForwardRunResult) -> dict:
    return {
        "run_id": result.run_id,
        "run_name": result.run_name,
        "status": result.status.value if isinstance(result.status, WalkForwardRunStatus) else result.status,
        "request": walk_forward_run_request_to_dict(result.request),
        "windows": [walk_forward_window_to_dict(w) for w in result.windows],
        "window_results": [walk_forward_window_result_to_dict(wr) for wr in result.window_results],
        "aggregate_metrics": result.aggregate_metrics,
        "stability_bucket": result.stability_bucket.value if isinstance(result.stability_bucket, WalkForwardStabilityBucket) else result.stability_bucket,
        "oos_bucket": result.oos_bucket.value if isinstance(result.oos_bucket, OutOfSampleResultBucket) else result.oos_bucket,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors,
        "created_at_utc": result.created_at_utc
    }
