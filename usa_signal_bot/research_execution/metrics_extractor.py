from typing import Any
from usa_signal_bot.research_execution.execution_models import ResearchRun
from usa_signal_bot.core.exceptions import MetricsExtractionError

def extract_common_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    metrics = payload.get("metrics", {})
    if not metrics and "total_net_pnl_usd" in payload:
        metrics = payload

    extracted = {}
    for rm in required_comparison_metrics():
        if rm in metrics:
            extracted[rm] = normalize_metric_value(metrics[rm])

    return extracted

def extract_metrics_from_research_run(run: ResearchRun) -> dict[str, Any]:
    return extract_common_metrics(run.metrics)

def normalize_metric_value(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def required_comparison_metrics() -> list[str]:
    return [
        "total_net_pnl_usd",
        "total_gross_pnl_usd",
        "max_drawdown_pct",
        "win_rate_pct",
        "cost_drag_pct",
        "turnover_pct",
        "trade_count",
        "walk_forward_pass_ratio",
        "robustness_score"
    ]

def metrics_quality_warnings(metrics: dict[str, Any]) -> list[str]:
    warnings = []
    for rm in required_comparison_metrics():
        if rm not in metrics or metrics[rm] is None:
            warnings.append(f"Missing required metric: {rm}")
    return warnings

def metrics_extractor_to_text(metrics: dict[str, Any]) -> str:
    lines = ["--- EXTRACTED METRICS ---"]
    for k, v in metrics.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)
