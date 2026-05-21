from typing import Any

def extract_paper_metrics(paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "paper_snapshot_available": bool(paper_snapshot),
        **extract_paper_position_metrics(paper_snapshot),
        **extract_paper_signal_metrics(paper_snapshot),
        **extract_paper_safety_metrics(paper_snapshot)
    }

def extract_paper_position_metrics(paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "paper_position_count": paper_snapshot.get("position_count", 0),
        "paper_cash_usd": paper_snapshot.get("cash_usd", 0.0),
        "paper_equity_usd": paper_snapshot.get("equity_usd", 0.0)
    }

def extract_paper_signal_metrics(paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"paper_signal_count": paper_snapshot.get("signal_count", 0)}

def extract_paper_safety_metrics(paper_snapshot: dict[str, Any]) -> dict[str, int]:
    return {
        "paper_state_mutation_flag": int(paper_snapshot.get("paper_state_committed", False)),
        "paper_order_executed_flag": int(paper_snapshot.get("paper_order_executed", False))
    }

def required_paper_metrics() -> list[str]:
    return [
        "paper_position_count", "paper_signal_count", "paper_cash_usd",
        "paper_equity_usd", "paper_state_mutation_flag", "paper_order_executed_flag",
        "paper_snapshot_available"
    ]

def paper_metric_quality_warnings(metrics: dict[str, Any]) -> list[str]:
    warnings = []
    if not metrics.get("paper_snapshot_available"):
        warnings.append("Paper snapshot not available.")
    return warnings

def paper_metric_extractor_to_text(metrics: dict[str, Any]) -> str:
    return str(metrics)
