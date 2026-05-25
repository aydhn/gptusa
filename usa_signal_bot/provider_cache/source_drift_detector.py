from typing import Any
from usa_signal_bot.provider_cache.phase108_models import SourceComparisonResult

def detect_source_outliers(comparison_result: SourceComparisonResult) -> list[str]:
    return comparison_result.outlier_sources

def detect_source_drift_warnings(comparison_result: SourceComparisonResult) -> list[str]:
    return comparison_result.drift_warnings

def source_disagreement_score(metrics: dict[str, Any]) -> float | None:
    return metrics.get("close_diff_pct")

def source_drift_detector_summary(comparison_result: SourceComparisonResult) -> dict[str, Any]:
    return {"outliers": len(comparison_result.outlier_sources)}

def source_drift_detector_to_text(comparison_result: SourceComparisonResult) -> str:
    return f"Drift Detector - Outliers: {len(comparison_result.outlier_sources)}"
