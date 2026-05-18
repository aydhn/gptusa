from typing import Any

def ingest_comparison_report(payload: dict[str, Any]) -> dict[str, Any]:
    return payload

def extract_comparison_ids(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "baseline_run_id": payload.get("baseline_run_id"),
        "candidate_run_id": payload.get("candidate_run_id"),
        "experiment_id": payload.get("experiment_id")
    }

def extract_comparison_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("metrics", {})

def extract_gate_evaluations(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("gates", [])

def extract_attribution_delta(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("attribution_delta", {})

def extract_diagnostics_delta(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("diagnostics_delta", {})

def comparison_ingestion_warnings(payload: dict[str, Any]) -> list[str]:
    warnings = []
    if not payload.get("baseline_run_id"): warnings.append("Missing baseline_run_id")
    if not payload.get("candidate_run_id"): warnings.append("Missing candidate_run_id")
    if not payload.get("metrics"): warnings.append("Missing metrics")
    if not payload.get("gates"): warnings.append("Missing gates")
    return warnings

def comparison_ingestion_to_text(payload: dict[str, Any]) -> str:
    return "Comparison Ingestion Data"
