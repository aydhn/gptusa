import datetime
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    RuntimeMode,
    RuntimeRunStatus,
    PipelineStepName,
    PipelineStepStatus,
    ScanScope,
    ScanOutputLevel,
    RetryPolicy,
)

@dataclass
class PipelineStepConfig:
    step_name: PipelineStepName
    enabled: bool = True
    required: bool = True
    timeout_seconds: Optional[int] = None
    retry_policy: RetryPolicy = RetryPolicy.NONE
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PipelineStepResult:
    step_name: PipelineStepName
    status: PipelineStepStatus
    started_at_utc: Optional[str] = None
    completed_at_utc: Optional[str] = None
    duration_seconds: Optional[float] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class RuntimeState:
    run_id: str
    mode: RuntimeMode
    status: RuntimeRunStatus
    started_at_utc: Optional[str] = None
    completed_at_utc: Optional[str] = None
    current_step: Optional[PipelineStepName] = None
    step_results: List[PipelineStepResult] = field(default_factory=list)
    lock_path: Optional[str] = None
    stop_requested: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class MarketScanRequest:
    run_name: str
    mode: RuntimeMode
    scope: ScanScope
    symbols: Optional[List[str]] = None
    timeframes: List[str] = field(default_factory=lambda: ["1d"])
    provider_name: str = "yfinance"
    composite_set_name: str = "core"
    rule_strategy_set_name: str = "basic_rules"
    max_symbols: Optional[int] = None
    refresh_data: bool = False
    write_outputs: bool = True
    output_level: ScanOutputLevel = ScanOutputLevel.NORMAL
    dry_run: bool = False
    notify: bool = False
    notification_channel: str = 'dry_run'
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MarketScanResult:
    run_id: str
    created_at_utc: str
    request: MarketScanRequest
    status: RuntimeRunStatus
    resolved_symbols: List[str] = field(default_factory=list)
    step_results: List[PipelineStepResult] = field(default_factory=list)
    signal_count: int = 0
    candidate_count: int = 0
    risk_approved_count: int = 0
    portfolio_allocation_count: int = 0
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class ScheduledScanPlan:
    plan_id: str
    enabled: bool
    name: str
    mode: RuntimeMode
    interval_minutes: int
    max_runs_per_day: int
    market_hours_only: bool
    timezone: str
    scan_request_template: MarketScanRequest
    created_at_utc: str
    metadata: Dict[str, Any] = field(default_factory=dict)

def pipeline_step_config_to_dict(config: PipelineStepConfig) -> dict:
    return {
        "step_name": config.step_name.value if isinstance(config.step_name, PipelineStepName) else config.step_name,
        "enabled": config.enabled,
        "required": config.required,
        "timeout_seconds": config.timeout_seconds,
        "retry_policy": config.retry_policy.value if isinstance(config.retry_policy, RetryPolicy) else config.retry_policy,
        "metadata": config.metadata,
    }

def pipeline_step_result_to_dict(result: PipelineStepResult) -> dict:
    return {
        "step_name": result.step_name.value if isinstance(result.step_name, PipelineStepName) else result.step_name,
        "status": result.status.value if isinstance(result.status, PipelineStepStatus) else result.status,
        "started_at_utc": result.started_at_utc,
        "completed_at_utc": result.completed_at_utc,
        "duration_seconds": result.duration_seconds,
        "output_paths": result.output_paths,
        "summary": result.summary,
        "warnings": result.warnings,
        "errors": result.errors,
    }

def runtime_state_to_dict(state: RuntimeState) -> dict:
    return {
        "run_id": state.run_id,
        "mode": state.mode.value if isinstance(state.mode, RuntimeMode) else state.mode,
        "status": state.status.value if isinstance(state.status, RuntimeRunStatus) else state.status,
        "started_at_utc": state.started_at_utc,
        "completed_at_utc": state.completed_at_utc,
        "current_step": state.current_step.value if isinstance(state.current_step, PipelineStepName) else state.current_step,
        "step_results": [pipeline_step_result_to_dict(r) for r in state.step_results],
        "lock_path": state.lock_path,
        "stop_requested": state.stop_requested,
        "warnings": state.warnings,
        "errors": state.errors,
    }

def market_scan_request_to_dict(request: MarketScanRequest) -> dict:
    return {
        "run_name": request.run_name,
        "mode": request.mode.value if isinstance(request.mode, RuntimeMode) else request.mode,
        "scope": request.scope.value if isinstance(request.scope, ScanScope) else request.scope,
        "symbols": request.symbols,
        "timeframes": request.timeframes,
        "provider_name": request.provider_name,
        "composite_set_name": request.composite_set_name,
        "rule_strategy_set_name": request.rule_strategy_set_name,
        "max_symbols": request.max_symbols,
        "refresh_data": request.refresh_data,
        "write_outputs": request.write_outputs,
        "output_level": request.output_level.value if isinstance(request.output_level, ScanOutputLevel) else request.output_level,
        "dry_run": request.dry_run,
        "notify": request.notify,
        "notification_channel": request.notification_channel,
        "metadata": request.metadata,
    }

def market_scan_result_to_dict(result: MarketScanResult) -> dict:
    return {
        "run_id": result.run_id,
        "created_at_utc": result.created_at_utc,
        "request": market_scan_request_to_dict(result.request),
        "status": result.status.value if isinstance(result.status, RuntimeRunStatus) else result.status,
        "resolved_symbols": result.resolved_symbols,
        "step_results": [pipeline_step_result_to_dict(r) for r in result.step_results],
        "signal_count": result.signal_count,
        "candidate_count": result.candidate_count,
        "risk_approved_count": result.risk_approved_count,
        "portfolio_allocation_count": result.portfolio_allocation_count,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors,
    }

def scheduled_scan_plan_to_dict(plan: ScheduledScanPlan) -> dict:
    return {
        "plan_id": plan.plan_id,
        "enabled": plan.enabled,
        "name": plan.name,
        "mode": plan.mode.value if isinstance(plan.mode, RuntimeMode) else plan.mode,
        "interval_minutes": plan.interval_minutes,
        "max_runs_per_day": plan.max_runs_per_day,
        "market_hours_only": plan.market_hours_only,
        "timezone": plan.timezone,
        "scan_request_template": market_scan_request_to_dict(plan.scan_request_template),
        "created_at_utc": plan.created_at_utc,
        "metadata": plan.metadata,
    }

def validate_pipeline_step_config(config: PipelineStepConfig) -> None:
    pass

def validate_market_scan_request(request: MarketScanRequest) -> None:
    if not request.run_name:
        raise ValueError("run_name cannot be empty")
    if not request.timeframes:
        raise ValueError("timeframes cannot be empty")
    if not request.provider_name:
        raise ValueError("provider_name cannot be empty")
    if request.max_symbols is not None and request.max_symbols <= 0:
        raise ValueError("max_symbols must be None or positive")

def validate_scheduled_scan_plan(plan: ScheduledScanPlan) -> None:
    if plan.interval_minutes <= 0:
        raise ValueError("interval_minutes must be positive")
    if plan.max_runs_per_day <= 0:
        raise ValueError("max_runs_per_day must be positive")
    validate_market_scan_request(plan.scan_request_template)

def create_runtime_run_id(prefix: str = "scan") -> str:
    return f"{prefix}_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

def create_scheduled_scan_plan_id(prefix: str = "plan") -> str:
    return f"{prefix}_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
