import json
from pathlib import Path
from typing import Optional

from usa_signal_bot.runtime.runtime_models import (
    MarketScanRequest, MarketScanResult, PipelineStepResult, RuntimeState, ScheduledScanPlan
)
from usa_signal_bot.runtime.runtime_validation import RuntimeValidationReport

def pipeline_step_result_to_text(result: PipelineStepResult) -> str:
    status_str = result.status.value if hasattr(result.status, "value") else result.status
    step_str = result.step_name.value if hasattr(result.step_name, "value") else result.step_name
    dur_str = f"{result.duration_seconds:.2f}s" if result.duration_seconds is not None else "N/A"
    lines = [f"Step: {step_str} | Status: {status_str} | Duration: {dur_str}"]
    if result.warnings:
        lines.append(f"  Warnings: {len(result.warnings)}")
    if result.errors:
        lines.append(f"  Errors: {len(result.errors)}")
        for e in result.errors[:3]:
            lines.append(f"    - {e}")
    return "\n".join(lines)

def market_scan_request_to_text(request: MarketScanRequest) -> str:
    scope_str = request.scope.value if hasattr(request.scope, "value") else request.scope
    mode_str = request.mode.value if hasattr(request.mode, "value") else request.mode
    return (
        f"Scan Request [{request.run_name}]\n"
        f"Mode: {mode_str} | Scope: {scope_str}\n"
        f"Timeframes: {', '.join(request.timeframes)}\n"
        f"Provider: {request.provider_name} | Dry Run: {request.dry_run}"
    )

def market_scan_result_to_text(result: MarketScanResult, limit: int = 30) -> str:
    status_str = result.status.value if hasattr(result.status, "value") else result.status
    lines = [
        f"--- MARKET SCAN RESULT: {result.run_id} ---",
        f"Status: {status_str}",
        f"Created: {result.created_at_utc}",
        f"Resolved Symbols: {len(result.resolved_symbols)}",
        f"Signals: {result.signal_count} | Candidates: {result.candidate_count} | Allocations: {result.portfolio_allocation_count}",
        "",
        "--- PIPELINE STEPS ---"
    ]
    for r in result.step_results:
        lines.append(pipeline_step_result_to_text(r))

    lines.append("")
    lines.append(runtime_limitations_text())
    return "\n".join(lines)

def runtime_state_to_text(state: RuntimeState) -> str:
    status_str = state.status.value if hasattr(state.status, "value") else state.status
    curr_str = state.current_step.value if state.current_step and hasattr(state.current_step, "value") else str(state.current_step)
    return (
        f"Runtime State [{state.run_id}]\n"
        f"Status: {status_str} | Current Step: {curr_str} | Stop Requested: {state.stop_requested}"
    )

def scan_summary_to_text(result: MarketScanResult) -> str:
    status_str = result.status.value if hasattr(result.status, "value") else result.status
    return f"Scan {result.run_id} ({status_str}) - Symbols: {len(result.resolved_symbols)}, Candidates: {result.candidate_count}"

def scheduled_scan_plan_summary_to_text(plan: ScheduledScanPlan) -> str:
    return f"Plan {plan.plan_id} - {plan.name} (Enabled: {plan.enabled}, Interval: {plan.interval_minutes}m)"

def runtime_limitations_text() -> str:
    return (
        "*** RUNTIME LIMITATIONS ***\n"
        "- This scan result is NOT investment advice.\n"
        "- No live, demo, or paper trades were executed.\n"
        "- No broker API interactions occurred.\n"
        "- Telegram notifications are not sent in this phase."
    )

def write_scan_report_json(path: Path, result: MarketScanResult, validation_report: Optional[RuntimeValidationReport] = None) -> Path:
    report = {
        "text": market_scan_result_to_text(result),
        "run_id": result.run_id,
        "validation_passed": validation_report.valid if validation_report else None
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    return path
