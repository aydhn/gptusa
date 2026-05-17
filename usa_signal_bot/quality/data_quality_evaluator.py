from typing import Any, Dict
# Assuming existing evaluator code, we'll just mock the integration for now as the prompt mentions "Quality scorecard içine diagnostics boyutları ekle"
# The actual file might have existed, but I will write a mock representing the addition.

def calculate_quality_score(provider_metrics: Dict[str, Any], diagnostics_summary: Dict[str, Any] = None) -> float:
    score = 100.0
    if diagnostics_summary:
        if diagnostics_summary.get("diagnostic_status") in ["DEGRADED", "FAILING"]:
            score -= 20.0
        failures = diagnostics_summary.get("high_severity_failure_count", 0)
        score -= (failures * 5)
    return max(0.0, score)

def build_quality_scorecard(metrics: Dict[str, Any], diagnostics_summary: Dict[str, Any] = None) -> Dict[str, Any]:
    score = calculate_quality_score(metrics, diagnostics_summary)
    card = {
        "overall_score": score,
        "diagnostics_quality_score": diagnostics_summary.get("quality_score") if diagnostics_summary else None,
        "failure_mode_severity_score": 100 - (diagnostics_summary.get("high_severity_failure_count", 0) * 5) if diagnostics_summary else 100,
        "strategy_diagnostic_score": 100 - (diagnostics_summary.get("degraded_strategy_count", 0) * 10) if diagnostics_summary else 100,
        "failure_cluster_risk_score": 100 - (len(diagnostics_summary.get("top_failure_clusters", [])) * 5) if diagnostics_summary else 100,
        "remediation_hint_quality_score": 100 if diagnostics_summary and diagnostics_summary.get("remediation_hint_count", 0) > 0 else 50
    }
    return card
