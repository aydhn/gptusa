from typing import Dict, Any, List, Optional
from usa_signal_bot.core.enums import PerformanceBaselineScope, BaselineComparisonStatus
from usa_signal_bot.performance.baseline_models import PerformanceBaseline, CurrentPerformanceSample, PerformanceReviewResult
from usa_signal_bot.performance.baseline_builder import build_performance_baseline
from usa_signal_bot.performance.baseline_collectors import normalize_profile_to_sample

def performance_samples_from_resource_profiles(profiles: List[Any]) -> List[CurrentPerformanceSample]:
    samples = []
    for p in profiles:
        try:
            if isinstance(p, dict):
                samples.append(normalize_profile_to_sample(p))
            elif hasattr(p, '__dict__'):
                samples.append(normalize_profile_to_sample(p.__dict__))
        except Exception:
            continue
    return samples

def performance_baseline_from_resource_profiles(scope: PerformanceBaselineScope, profiles: List[Any]) -> PerformanceBaseline:
    samples = performance_samples_from_resource_profiles(profiles)
    return build_performance_baseline(scope, samples)

def profiling_calibration_hints_from_performance_review(review: PerformanceReviewResult) -> Dict[str, Any]:
    hints = {
        "action": "KEEP_CURRENT",
        "reason": "Performance within normal parameters."
    }

    if review.acceptance_status == BaselineComparisonStatus.BLOCKED:
        hints["action"] = "DELAY"
        hints["reason"] = "Performance gate BLOCKED, pausing workloads."
    elif review.acceptance_status == BaselineComparisonStatus.FAIL:
        hints["action"] = "REDUCE_SCOPE"
        hints["reason"] = "Performance gate FAIL, reducing workload scope."
    elif review.acceptance_status == BaselineComparisonStatus.WARN:
        hints["action"] = "WARN"
        hints["reason"] = "Performance gate WARN, monitoring closely."

    return hints

def profiling_adapter_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Profiling Adapter Summary:\n{summary}"
