import json
from pathlib import Path
from typing import List, Optional, Any, Dict
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

from usa_signal_bot.strategies.signal_scoring import SignalScoringResult
from usa_signal_bot.strategies.signal_quality import SignalQualityReport, quality_report_to_text
from usa_signal_bot.strategies.signal_confluence import ConfluenceReport, confluence_report_to_text
from usa_signal_bot.strategies.signal_store import write_signal_quality_report_json, write_confluence_report_json, build_signal_report_path

def signal_scoring_result_to_text(result: SignalScoringResult) -> str:
    lines = [
        f"Signal ID: {result.original_signal.signal_id}",
        f"Symbol: {result.original_signal.symbol} | Action: {result.original_signal.action.value if hasattr(result.original_signal.action, 'value') else result.original_signal.action}",
        f"Accepted for Review: {result.accepted_for_review}",
        f"Final Score: {result.breakdown.total_score:.1f} | Final Confidence: {result.breakdown.final_confidence:.2f}",
        f"Confidence Bucket: {result.breakdown.confidence_bucket.value if hasattr(result.breakdown.confidence_bucket, 'value') else result.breakdown.confidence_bucket}",
        "Breakdown:"
    ]
    for comp, val in result.breakdown.components.items():
        lines.append(f"  + {comp}: {val:.1f}")
    for pen, val in result.breakdown.penalties.items():
        lines.append(f"  - {pen}: {val:.1f}")
    for bon, val in result.breakdown.bonuses.items():
        lines.append(f"  + {bon}: {val:.1f}")

    if result.breakdown.notes:
        lines.append("Notes:")
        for n in result.breakdown.notes:
            lines.append(f"  * {n}")

    if result.warnings:
        lines.append("Warnings:")
        for w in result.warnings:
            lines.append(f"  ! {w}")

    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f"  X {e}")

    return "\n".join(lines)

def signal_scoring_results_to_text(results: List[SignalScoringResult], limit: int = 20) -> str:
    if not results:
        return "No scoring results to display."

    lines = [f"--- Scoring Results Summary ({len(results)} signals) ---"]
    accepted = sum(1 for r in results if r.accepted_for_review)
    lines.append(f"Accepted for Review: {accepted}/{len(results)}")
    lines.append("")

    for i, res in enumerate(results[:limit]):
        lines.append(signal_scoring_result_to_text(res))
        lines.append("-" * 40)

    if len(results) > limit:
        lines.append(f"... and {len(results) - limit} more signals.")

    return "\n".join(lines)

def write_full_strategy_quality_report_json(
    data_root: Path,
    run_result: StrategyRunResult,
    scoring_results: List[SignalScoringResult],
    quality_report: SignalQualityReport,
    confluence_report: Optional[ConfluenceReport] = None
) -> Dict[str, Path]:

    written_paths = {}

    # Write quality report
    qr_path = build_signal_report_path(data_root, f"quality_{run_result.strategy_name}", run_result.run_id)
    write_signal_quality_report_json(qr_path, quality_report)
    written_paths["quality_report"] = qr_path

    # Write confluence report if exists
    if confluence_report:
        cr_path = build_signal_report_path(data_root, f"confluence_{run_result.strategy_name}", run_result.run_id)
        write_confluence_report_json(cr_path, confluence_report)
        written_paths["confluence_report"] = cr_path

    return written_paths
