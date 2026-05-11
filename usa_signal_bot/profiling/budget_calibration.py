from typing import Any
import statistics

from usa_signal_bot.core.enums import ResourceProfileScope, CalibrationStatus, CalibrationDecision
from usa_signal_bot.profiling.profiling_models import ResourceProfile, BudgetCalibrationResult, create_budget_calibration_id
from usa_signal_bot.profiling.resource_timer import current_utc_iso

def calculate_profile_percentiles(values: list[float], percentiles: list[float] | None = None) -> dict[str, float]:
    if not values:
        return {}

    if percentiles is None:
        percentiles = [50.0, 75.0, 90.0, 95.0, 99.0]

    sorted_vals = sorted(values)
    n = len(sorted_vals)

    result = {}
    for p in percentiles:
        idx = int(p / 100.0 * (n - 1))
        result[f"p{int(p)}"] = sorted_vals[idx]

    return result

def confidence_from_sample_count(sample_count: int) -> float:
    if sample_count == 0:
        return 0.0
    if sample_count < 3:
        return 0.2
    if sample_count < 10:
        return 0.5
    if sample_count < 30:
        return 0.8
    return 0.95

def decide_calibration_action(current_budget: dict[str, Any], recommended_budget: dict[str, Any], sample_count: int) -> CalibrationDecision:
    if sample_count < 3:
        return CalibrationDecision.REVIEW_REQUIRED

    curr_time = current_budget.get("wall_time_seconds", 0)
    rec_time = recommended_budget.get("wall_time_seconds", 0)

    if rec_time > curr_time * 1.5:
        return CalibrationDecision.SPLIT_TASK
    elif rec_time > curr_time:
        return CalibrationDecision.RAISE_BUDGET
    elif rec_time < curr_time * 0.5:
        return CalibrationDecision.LOWER_BUDGET

    return CalibrationDecision.KEEP_CURRENT

def recommend_budget_from_profiles(profiles: list[ResourceProfile], current_budget: dict[str, Any]) -> dict[str, Any]:
    wall_times = [p.wall_time_seconds for p in profiles if p.wall_time_seconds is not None]
    mem_peaks = [p.memory_peak_bytes for p in profiles if p.memory_peak_bytes is not None]

    rec_budget = dict(current_budget)

    if len(wall_times) >= 3:
        p90_time = calculate_profile_percentiles(wall_times, [90.0]).get("p90", 0)
        rec_budget["wall_time_seconds"] = p90_time * 1.2

    if len(mem_peaks) >= 3:
        p90_mem = calculate_profile_percentiles(mem_peaks, [90.0]).get("p90", 0)
        rec_budget["memory_peak_bytes"] = p90_mem * 1.2

    return rec_budget

def calibrate_budget_for_scope(scope: ResourceProfileScope, profiles: list[ResourceProfile], current_budget: dict[str, Any]) -> BudgetCalibrationResult:
    scope_profiles = [p for p in profiles if p.scope == scope]
    sample_count = len(scope_profiles)

    status = CalibrationStatus.INSUFFICIENT_DATA
    decision = CalibrationDecision.REVIEW_REQUIRED
    recommended = current_budget
    confidence = confidence_from_sample_count(sample_count)
    warnings = []

    if sample_count >= 3:
        status = CalibrationStatus.CALIBRATED
        recommended = recommend_budget_from_profiles(scope_profiles, current_budget)
        decision = decide_calibration_action(current_budget, recommended, sample_count)
    else:
        warnings.append(f"Not enough samples ({sample_count}) for scope {scope.value} to calibrate reliably.")

    return BudgetCalibrationResult(
        calibration_id=create_budget_calibration_id(),
        created_at_utc=current_utc_iso(),
        status=status,
        scope=scope,
        sample_count=sample_count,
        decision=decision,
        current_budget=current_budget,
        recommended_budget=recommended,
        confidence=confidence,
        evidence={"profiles_analyzed": sample_count},
        warnings=warnings,
        errors=[]
    )

def calibrate_all_budgets(profiles: list[ResourceProfile], current_budgets: dict[str, dict[str, Any]]) -> list[BudgetCalibrationResult]:
    results = []
    for scope_str, budget in current_budgets.items():
        try:
            scope = ResourceProfileScope(scope_str)
            result = calibrate_budget_for_scope(scope, profiles, budget)
            results.append(result)
        except ValueError:
            pass
    return results

def budget_calibration_result_to_text(result: BudgetCalibrationResult) -> str:
    lines = [
        f"Calibration for {result.scope.value} (Samples: {result.sample_count})",
        f"Status: {result.status.value}",
        f"Decision: {result.decision.value}",
        f"Confidence: {result.confidence:.2f}" if result.confidence is not None else "Confidence: N/A"
    ]
    return "\n".join(lines)
