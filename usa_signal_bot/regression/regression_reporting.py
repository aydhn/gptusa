from typing import Any, Dict
from pathlib import Path

from usa_signal_bot.regression.regression_models import (
    GoldenDatasetSpec,
    GoldenSnapshot,
    RegressionStepResult,
    RegressionRunResult,
    ReleaseRehearsalResult
)
from usa_signal_bot.regression.regression_validation import RegressionValidationReport

def golden_dataset_spec_to_text(spec: GoldenDatasetSpec) -> str:
    return f"Dataset: {spec.name} ({spec.status.value}), Symbols: {len(spec.symbols)}, Timeframe: {spec.timeframe}, Rows: {spec.row_count_per_symbol}"

def golden_snapshot_to_text(snapshot: GoldenSnapshot) -> str:
    return f"Snapshot: {snapshot.name} [{snapshot.checksum[:8]}] created {snapshot.created_at_utc}"

def regression_step_result_to_text(result: RegressionStepResult) -> str:
    dur = f"{result.duration_seconds}s" if result.duration_seconds is not None else "N/A"
    return f"[{result.status.value}] {result.step_name.value} in {dur}"

def regression_run_result_to_text(result: RegressionRunResult, limit: int = 40) -> str:
    lines = [
        "=== Regression Run Report ===",
        f"ID: {result.run_id}",
        f"Status: {result.status.value}",
        f"Scope: {result.request.scope.value}",
        f"Dataset: {result.request.dataset_name}",
        "-" * 30,
        "Steps:"
    ]
    for s in result.step_results:
        lines.append("  " + regression_step_result_to_text(s))

    lines.append("-" * 30)
    lines.append(f"Snapshot Comparison: {result.snapshot_comparison.get('status', 'UNKNOWN')}")
    lines.append(f"Release Status: {result.release_candidate_status.value}")

    if result.errors:
        lines.append("Errors:")
        for e in result.errors[:limit]:
            lines.append(f"  - {e}")

    lines.append(regression_limitations_text())
    return "\n".join(lines)

def release_rehearsal_result_to_text(result: ReleaseRehearsalResult, limit: int = 40) -> str:
    lines = [
        "=== Release Candidate Rehearsal ===",
        f"ID: {result.rehearsal_id}",
        f"Status: {result.status.value}",
        f"Scope: {result.scope.value}",
        "-" * 30,
        f"Passed Steps: {result.passed_steps}",
        f"Failed Steps: {result.failed_steps}",
        "-" * 30
    ]
    if result.required_actions:
         lines.append("Required Actions:")
         for a in result.required_actions:
             lines.append(f"  [!] {a}")

    lines.append("\n" + regression_run_result_to_text(result.regression_result))
    return "\n".join(lines)

def snapshot_comparison_to_text(snapshot_comparison: Dict[str, Any]) -> str:
    status = snapshot_comparison.get('status', 'UNKNOWN')
    baseline = snapshot_comparison.get('baseline_checksum', 'None')
    current = snapshot_comparison.get('current_checksum', 'None')
    return f"Snapshot Status: {status} | Baseline: {baseline[:8] if baseline else 'None'} | Current: {current[:8] if current else 'None'}"

def regression_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Regression Store: {summary.get('runs_count', 0)} Runs, {summary.get('releases_count', 0)} Releases"

def regression_limitations_text() -> str:
    return (
        "\nIMPORTANT LIMITATIONS:\n"
        "- This is a LOCAL regression test using deterministic fixtures.\n"
        "- It does NOT use real market conditions or broker execution.\n"
        "- A PASS status is NOT an approval for live trading with real funds.\n"
        "- This report does NOT constitute investment advice."
    )

def write_regression_report_json(path: Path, result: RegressionRunResult, validation_report: RegressionValidationReport | None = None) -> Path:
    import json
    from usa_signal_bot.regression.regression_models import regression_run_result_to_dict
    from dataclasses import asdict

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "result": regression_run_result_to_dict(result),
        "validation": asdict(validation_report) if validation_report else None,
        "limitations": regression_limitations_text()
    }
    with open(path, "w") as f:
         json.dump(payload, f, indent=2)
    return path

def write_release_rehearsal_report_json(path: Path, result: ReleaseRehearsalResult, validation_report: RegressionValidationReport | None = None) -> Path:
    import json
    from usa_signal_bot.regression.regression_models import release_rehearsal_result_to_dict
    from dataclasses import asdict

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "result": release_rehearsal_result_to_dict(result),
        "validation": asdict(validation_report) if validation_report else None,
        "limitations": regression_limitations_text()
    }
    with open(path, "w") as f:
         json.dump(payload, f, indent=2)
    return path
