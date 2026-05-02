import json
from pathlib import Path
from typing import List, Optional, Any
from usa_signal_bot.strategies.strategy_models import StrategyRunResult, StrategyExecutionSummary, summarize_strategy_run
from usa_signal_bot.strategies.signal_contract import StrategySignal, signal_to_text
from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
from usa_signal_bot.strategies.signal_validation import SignalValidationReport

def strategy_run_result_to_text(result: StrategyRunResult) -> str:
    summary = summarize_strategy_run(result)
    return strategy_execution_summary_to_text(summary)

def strategy_execution_summary_to_text(summary: StrategyExecutionSummary) -> str:
    lines = [
        f"--- Strategy Execution Summary ---",
        f"Strategy: {summary.strategy_name}",
        f"Run ID: {summary.run_id}",
        f"Total Signals: {summary.total_signals}"
    ]

    if summary.total_signals > 0:
        lines.append(f"  LONG: {summary.long_count}")
        lines.append(f"  SHORT: {summary.short_count}")
        lines.append(f"  FLAT: {summary.flat_count}")
        lines.append(f"  WATCH: {summary.watch_count}")
        lines.append(f"  AVOID: {summary.avoid_count}")
        if summary.average_confidence is not None:
            lines.append(f"  Average Confidence: {summary.average_confidence:.2f}")

    if summary.errors:
        lines.append("Errors:")
        for e in summary.errors:
            lines.append(f"  - {e}")

    if summary.warnings:
        lines.append("Warnings:")
        for w in summary.warnings:
            lines.append(f"  - {w}")

    return "\n".join(lines)

def strategy_signal_list_to_text(signals: List[StrategySignal], limit: int = 20) -> str:
    if not signals:
        return "No signals generated."

    lines = [f"--- Signal List (Showing up to {limit}) ---"]
    for i, sig in enumerate(signals[:limit]):
        lines.append(signal_to_text(sig))
        if i < min(len(signals), limit) - 1:
            lines.append("-" * 40)

    if len(signals) > limit:
        lines.append(f"... and {len(signals) - limit} more signals.")

    return "\n".join(lines)

def strategy_registry_to_text(registry: StrategyRegistry) -> str:
    lines = ["--- Strategy Registry ---"]
    metadata_list = registry.list_metadata()

    if not metadata_list:
        lines.append("No strategies registered.")
        return "\n".join(lines)

    for meta in metadata_list:
        lines.append(f"[{meta.category.value if hasattr(meta.category, 'value') else meta.category}] {meta.name} (v{meta.version})")
        lines.append(f"  Status: {meta.status.value if hasattr(meta.status, 'value') else meta.status} | Experimental: {meta.experimental}")
        lines.append(f"  Required Features: {meta.required_features}")

    return "\n".join(lines)

def write_strategy_run_report_json(path: Path, result: StrategyRunResult, validation_report: Optional[SignalValidationReport] = None) -> Path:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        summary = summarize_strategy_run(result)

        d = {
            "run_id": summary.run_id,
            "strategy_name": summary.strategy_name,
            "total_signals": summary.total_signals,
            "counts": {
                "LONG": summary.long_count,
                "SHORT": summary.short_count,
                "FLAT": summary.flat_count,
                "WATCH": summary.watch_count,
                "AVOID": summary.avoid_count
            },
            "average_confidence": summary.average_confidence,
            "warnings": summary.warnings,
            "errors": summary.errors
        }

        if validation_report:
            d["validation"] = {
                "valid": validation_report.valid,
                "invalid_signals": validation_report.invalid_signals
            }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

        return path
    except Exception as e:
        print(f"Failed to write run report to {path}: {e}")
        return path
