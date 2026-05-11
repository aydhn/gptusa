from pathlib import Path
from typing import Any

from usa_signal_bot.profiling.profiling_models import (
    ResourceMetric,
    ResourceProfile,
    BudgetCalibrationResult,
    ThrottlingRecommendation,
    ThrottlingPlan,
    ProfilingReviewResult
)
from usa_signal_bot.profiling.profiling_validation import ProfilingValidationReport
from usa_signal_bot.profiling.profiling_store import write_profiling_review_result_json

def resource_metric_to_text(metric: ResourceMetric) -> str:
    return f"Metric: {metric.name.value} = {metric.value} {metric.unit or ''} [{metric.status.value}]"

def resource_profile_to_text(profile: ResourceProfile) -> str:
    lines = [
        f"Resource Profile: {profile.target_name} ({profile.scope.value})",
        f"Status: {profile.status.value}",
        f"Wall Time: {profile.wall_time_seconds:.2f}s" if profile.wall_time_seconds is not None else "Wall Time: N/A",
        f"Peak Memory: {profile.memory_peak_bytes / (1024*1024):.2f} MB" if profile.memory_peak_bytes is not None else "Peak Memory: N/A",
        f"Output Growth: {profile.output_growth_bytes / (1024*1024):.2f} MB" if profile.output_growth_bytes is not None else "Output Growth: N/A"
    ]
    return "\n".join(lines)

def budget_calibration_result_to_text(result: BudgetCalibrationResult) -> str:
    lines = [
        f"Calibration Result: {result.scope.value} (Samples: {result.sample_count})",
        f"Status: {result.status.value}",
        f"Decision: {result.decision.value}"
    ]
    return "\n".join(lines)

def throttling_recommendation_to_text(rec: ThrottlingRecommendation) -> str:
    return f"Recommendation [{rec.severity.value}]: {rec.action.value} - {rec.message}"

def throttling_plan_to_text(plan: ThrottlingPlan, limit: int = 50) -> str:
    lines = [
        "Throttling Plan:",
        f"Status: {plan.status.value}",
        f"Blocked: {plan.blocked_count}, Warnings: {plan.warning_count}, Reviews: {plan.review_count}",
        "Recommendations:"
    ]
    for i, r in enumerate(plan.recommendations[:limit]):
        lines.append(f"  {i+1}. {throttling_recommendation_to_text(r)}")

    if len(plan.recommendations) > limit:
        lines.append(f"  ... and {len(plan.recommendations) - limit} more.")

    lines.append("\n" + profiling_limitations_text())
    return "\n".join(lines)

def profiling_review_result_to_text(result: ProfilingReviewResult, limit: int = 50) -> str:
    lines = [
        f"Profiling Review Result: {result.report_type.value}",
        f"Status: {result.status.value}",
        f"Profiles Evaluated: {len(result.profiles)}",
        f"Calibrations Performed: {len(result.calibration_results)}"
    ]

    if result.throttling_plan:
        lines.append("\n" + throttling_plan_to_text(result.throttling_plan, limit))

    lines.append("\n" + profiling_limitations_text())
    return "\n".join(lines)

def profiling_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = ["Profiling Store Summary:"]
    for k, v in summary.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)

def profiling_limitations_text() -> str:
    return (
        "*** DISCLAIMER & LIMITATIONS ***\n"
        "- This is a LOCAL resource profile. NO external telemetry is used.\n"
        "- Measurements are APPROXIMATE. Memory tracing evaluates Python allocations, not total OS ram.\n"
        "- Throttling decisions are LOCAL OPERATIONAL rules, and do NOT constitute investment advice.\n"
        "- No live, real, or demo broker orders are generated or approved by these plans.\n"
        "********************************"
    )

def write_profiling_report_json(path: Path, result: ProfilingReviewResult, validation_report: ProfilingValidationReport | None = None) -> Path:
    if validation_report and not validation_report.valid:
        raise ValueError("Cannot write invalid profiling report to disk.")

    return write_profiling_review_result_json(path, result)
