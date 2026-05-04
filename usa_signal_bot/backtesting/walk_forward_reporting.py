import json
from pathlib import Path
from usa_signal_bot.backtesting.walk_forward_models import WalkForwardWindow, WalkForwardWindowResult, WalkForwardRunResult
from usa_signal_bot.backtesting.walk_forward_metrics import walk_forward_aggregate_metrics_to_text
from usa_signal_bot.backtesting.walk_forward_validation import WalkForwardValidationReport, walk_forward_validation_report_to_text

def walk_forward_window_to_text(window: WalkForwardWindow) -> str:
    return f"Window {window.window_id} ({window.mode}): Train [{window.train_start} -> {window.train_end}] Test [{window.test_start} -> {window.test_end}] - Status: {window.status}"

def walk_forward_window_result_to_text(result: WalkForwardWindowResult) -> str:
    lines = [walk_forward_window_to_text(result.window)]

    is_ret = result.in_sample_metrics.get('total_return_pct')
    oos_ret = result.out_of_sample_metrics.get('total_return_pct')

    is_str = f"{is_ret:.2f}%" if is_ret is not None else "N/A"
    oos_str = f"{oos_ret:.2f}%" if oos_ret is not None else "N/A"

    lines.append(f"  IS Return:  {is_str}")
    lines.append(f"  OOS Return: {oos_str}")

    if result.errors:
        lines.append(f"  Errors: {len(result.errors)}")

    return "\n".join(lines)

def walk_forward_summary_to_text(result: WalkForwardRunResult) -> str:
    lines = []
    lines.append("="*60)
    lines.append(f"WALK-FORWARD RUN SUMMARY: {result.run_name}")
    lines.append(f"ID: {result.run_id}")
    lines.append(f"Status: {result.status.value if hasattr(result.status, 'value') else result.status}")
    lines.append(f"Date: {result.created_at_utc}")
    lines.append("-" * 60)

    lines.append(walk_forward_aggregate_metrics_to_text(result.aggregate_metrics))

    lines.append("-" * 60)
    st = result.stability_bucket.value if hasattr(result.stability_bucket, 'value') else result.stability_bucket
    os = result.oos_bucket.value if hasattr(result.oos_bucket, 'value') else result.oos_bucket
    lines.append(f"Stability Classification: {st}")
    lines.append(f"OOS Classification:       {os}")

    if result.errors:
        lines.append("\nRun Errors:")
        for err in result.errors:
            lines.append(f"  - {err}")

    return "\n".join(lines)

def walk_forward_run_result_to_text(result: WalkForwardRunResult, limit: int = 20) -> str:
    lines = [walk_forward_summary_to_text(result)]

    lines.append("="*60)
    lines.append(f"WINDOW RESULTS (Showing up to {limit})")
    lines.append("-" * 60)

    for wr in result.window_results[:limit]:
        lines.append(walk_forward_window_result_to_text(wr))
        lines.append("")

    if len(result.window_results) > limit:
        lines.append(f"... and {len(result.window_results) - limit} more windows.")

    return "\n".join(lines)

def walk_forward_limitations_text() -> str:
    return """
WALK-FORWARD LIMITATIONS & DISCLAIMERS
--------------------------------------
1. Future Performance: Walk-forward analysis (including out-of-sample results)
   is strictly historical research. It does NOT guarantee future performance.
2. Optimization: This phase performs evaluation only. There is no parameter
   optimizer or search algorithm running.
3. Execution: Results are based on simulated market conditions without live
   or paper trading execution.
4. Costs: Transaction costs and slippage are hypothetical estimates.
5. Survivorship Bias: The current universe data may contain survivorship bias.
"""

def write_walk_forward_report_json(path: Path, result: WalkForwardRunResult, validation_report: WalkForwardValidationReport | None = None) -> Path:
    from usa_signal_bot.backtesting.walk_forward_store import _atomic_write_json
    from usa_signal_bot.backtesting.walk_forward_models import walk_forward_run_result_to_dict

    data = walk_forward_run_result_to_dict(result)
    data["report_text"] = walk_forward_run_result_to_text(result)
    if validation_report:
        data["validation"] = {
            "valid": validation_report.valid,
            "issues": len(validation_report.issues)
        }

    return _atomic_write_json(path, data)
