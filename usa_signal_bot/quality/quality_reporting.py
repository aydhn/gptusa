"""Quality System Reporting."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from usa_signal_bot.quality.quality_models import (
    QualityIssue,
    QualityDimensionScore,
    ResearchQualityScorecard,
    ProductionReadinessGateResult,
    SystemAcceptanceResult
)
from usa_signal_bot.quality.scorecard import scorecard_to_text
from usa_signal_bot.quality.readiness_gate import summarize_gate
from usa_signal_bot.quality.quality_validation import QualityValidationReport, quality_validation_report_to_text
from usa_signal_bot.quality.quality_store import (
    write_acceptance_result_json,
    write_quality_validation_report_json
)

def quality_issue_to_text(issue: QualityIssue) -> str:
    return f"[{issue.severity.name}] {issue.dimension.name}: {issue.title} - {issue.message}"

def quality_dimension_score_to_text(score: QualityDimensionScore) -> str:
    s = f"{score.score:.1f}" if score.score is not None else "N/A"
    return f"{score.dimension.name:<15}: {s:>5} [{score.status.name}]"

def research_quality_scorecard_to_text(scorecard: ResearchQualityScorecard, limit: int = 30) -> str:
    return scorecard_to_text(scorecard)

def production_readiness_gate_result_to_text(result: ProductionReadinessGateResult, limit: int = 30) -> str:
    return summarize_gate(result)

def system_acceptance_result_to_text(result: SystemAcceptanceResult, limit: int = 30) -> str:
    lines = [
        f"--- System Acceptance Result ({result.acceptance_id}) ---",
        f"Decision: {result.decision.name}",
        f"Scope: {result.scope.name}",
        f"Summary: {result.acceptance_summary}",
        ""
    ]
    if result.required_actions:
        lines.append("Required Actions:")
        for a in result.required_actions:
            lines.append(f" - {a}")
        lines.append("")
    if result.optional_actions:
        lines.append("Optional Actions:")
        for a in result.optional_actions:
            lines.append(f" - {a}")
        lines.append("")

    lines.append("--- IMPORTANT DISCLAIMER ---")
    lines.append("This is a local research evaluation only.")
    lines.append("It does NOT constitute live trading approval, broker validation, or investment advice.")

    return "\n".join(lines)

def quality_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Total Runs: {summary.get('total_runs', 0)}\nLatest Run: {summary.get('latest_run', 'None')}"

def quality_gate_limitations_text() -> str:
    return """QUALITY GATE LIMITATIONS
1. Quality score is NOT a guarantee of real performance.
2. Gate pass is NOT an approval for live trading.
3. Missing artifacts can lead to incomplete/incorrect scoring.
4. The system operates strictly as a local research tool with no broker integration.
5. Notification outputs do not constitute investment advice."""

def write_quality_report_json(path: Path, result: SystemAcceptanceResult, validation_report: Optional[QualityValidationReport] = None) -> Path:
    write_acceptance_result_json(path / "acceptance_result.json", result)
    if validation_report:
        try:
            write_quality_validation_report_json(path / "validation_report.json", {
                "valid": validation_report.valid,
                "error_count": validation_report.error_count,
                "errors": validation_report.errors
            })
        except Exception:
            pass
    return path
