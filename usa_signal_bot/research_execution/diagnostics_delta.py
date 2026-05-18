from typing import Any

def build_diagnostics_delta(baseline_payload: dict[str, Any] | None, candidate_payload: dict[str, Any] | None) -> dict[str, Any]:
    if not baseline_payload or not candidate_payload:
        return {"warning": "Missing diagnostics payloads for delta."}

    return {
        "scorecard_delta": compare_diagnostic_scorecards(baseline_payload.get("scorecard"), candidate_payload.get("scorecard")),
        "failure_mode_delta": compare_failure_mode_delta(baseline_payload.get("failure_modes"), candidate_payload.get("failure_modes")),
        "remediation_hint_delta": compare_remediation_hint_delta(baseline_payload.get("remediation_hints"), candidate_payload.get("remediation_hints"))
    }

def compare_diagnostic_scorecards(baseline: dict[str, Any] | None, candidate: dict[str, Any] | None) -> dict[str, Any]:
    if not baseline or not candidate:
        return {}
    return {k: candidate.get(k, 0) - baseline.get(k, 0) for k in baseline.keys() if isinstance(baseline[k], (int, float))}

def compare_failure_mode_delta(baseline: dict[str, Any] | None, candidate: dict[str, Any] | None) -> dict[str, Any]:
    return {}

def compare_remediation_hint_delta(baseline: dict[str, Any] | None, candidate: dict[str, Any] | None) -> dict[str, Any]:
    return {}

def diagnostics_delta_to_text(delta: dict[str, Any]) -> str:
    lines = ["--- DIAGNOSTICS DELTA ---"]
    if "warning" in delta:
        lines.append(delta["warning"])
    else:
        lines.append(f"Scorecard Delta: {delta.get('scorecard_delta')}")
    return "\n".join(lines)
