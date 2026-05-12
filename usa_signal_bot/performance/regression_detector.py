from typing import List, Optional, Tuple, Dict, Any

from usa_signal_bot.performance.baseline_models import PerformanceBaseline, CurrentPerformanceSample, BaselineComparisonResult
from usa_signal_bot.performance.threshold_models import SLAThreshold, SLAEvaluationReport
from usa_signal_bot.performance.baseline_comparator import compare_sample_to_baseline, find_baseline_for_sample
from usa_signal_bot.performance.threshold_evaluator import evaluate_thresholds
from usa_signal_bot.performance.drift_classifier import classify_baseline_drift, classify_runtime_regression

class RuntimeRegressionDetector:
    def __init__(self, baselines: List[PerformanceBaseline], thresholds: Optional[List[SLAThreshold]] = None):
        self.baselines = baselines
        self.thresholds = thresholds

    def detect(self, sample: CurrentPerformanceSample) -> Tuple[BaselineComparisonResult, SLAEvaluationReport]:
        baseline = find_baseline_for_sample(sample, self.baselines)

        comparison = compare_sample_to_baseline(sample, baseline)
        threshold_report = evaluate_thresholds(sample.scope, sample, baseline, self.thresholds)

        # update comparison with drift and regression
        comparison.drift_direction = classify_baseline_drift(comparison.metric_results)
        comparison.regression_status = classify_runtime_regression(comparison.metric_results, threshold_report)

        return comparison, threshold_report

    def detect_many(self, samples: List[CurrentPerformanceSample]) -> List[Dict[str, Any]]:
        results = []
        for sample in samples:
            comp, rep = self.detect(sample)
            results.append({
                "sample_id": sample.sample_id,
                "scope": sample.scope.value,
                "comparison": comp,
                "threshold_report": rep
            })
        return results

    def build_regression_alerts(self, samples: List[CurrentPerformanceSample]) -> List[Dict[str, Any]]:
        # A basic builder stub, full alerts constructed via alert_rules engine
        alerts = []
        for sample in samples:
            comp, rep = self.detect(sample)
            from usa_signal_bot.core.enums import RuntimeRegressionStatus
            if comp.regression_status in [RuntimeRegressionStatus.MAJOR_REGRESSION, RuntimeRegressionStatus.CRITICAL_REGRESSION]:
                alerts.append({
                    "sample_id": sample.sample_id,
                    "regression_status": comp.regression_status.value,
                    "metrics": comp.metric_results
                })
        return alerts

    def summarize_regressions(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        summary = {
            "total_checked": len(results),
            "no_regression": 0,
            "minor_regression": 0,
            "moderate_regression": 0,
            "major_regression": 0,
            "critical_regression": 0,
            "insufficient_data": 0
        }

        for r in results:
            status = r["comparison"].regression_status.value.lower()
            if status in summary:
                summary[status] += 1

        return summary
