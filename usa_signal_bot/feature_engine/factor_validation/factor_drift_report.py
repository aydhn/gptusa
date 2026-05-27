from typing import Any
from usa_signal_bot.feature_engine.factor_validation.phase122_models import FactorDriftReport, FactorDriftStatus

def build_factor_drift_report_summary(report: FactorDriftReport) -> dict[str, Any]:
    return {
        "symbol": report.symbol,
        "status": report.overall_drift_status.name,
        "max_drift": report.max_drift_score
    }

def build_factor_drift_reports_summary(reports: list[FactorDriftReport]) -> dict[str, Any]:
    return {
        "total": len(reports),
        "status_counts": drift_status_counts(reports)
    }

def factor_drift_report_to_text(report: FactorDriftReport, limit: int = 200) -> str:
    return f"Drift Report {report.symbol}: {report.overall_drift_status.name}"

def factor_drift_reports_to_text(reports: list[FactorDriftReport], limit: int = 300) -> str:
    return f"Generated {len(reports)} drift reports."

def drift_status_counts(reports: list[FactorDriftReport]) -> dict[str, int]:
    counts = {}
    for r in reports:
        n = r.overall_drift_status.name
        counts[n] = counts.get(n, 0) + 1
    return counts
