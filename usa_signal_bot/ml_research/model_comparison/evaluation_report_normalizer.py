from typing import Any, List

def normalize_evaluation_reports(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in reports]

def extract_metric_rows_from_reports(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for r in reports:
        for metric_name, metric_value in r.get("metrics", {}).items():
            rows.append({
                "metric_name": metric_name,
                "metric_value": metric_value,
                "model_artifact_id": r.get("model_artifact_id")
            })
    return rows

def validate_normalized_evaluation_rows(rows: list[dict[str, Any]]) -> list[str]:
    return []

def reject_trading_or_pnl_metrics(rows: list[dict[str, Any]]) -> list[str]:
    errors = []
    forbidden = ["pnl", "sharpe", "cagr", "max_drawdown"]
    for row in rows:
        name = row.get("metric_name", "").lower()
        if any(f in name for f in forbidden):
            errors.append(f"Forbidden trading metric: {name}")
    return errors

def evaluation_report_normalizer_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {"row_count": len(rows)}

def evaluation_report_normalizer_to_text(rows: list[dict[str, Any]], limit: int = 300) -> str:
    return str(rows)[:limit]
