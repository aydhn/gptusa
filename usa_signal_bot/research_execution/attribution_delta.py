from typing import Any

def build_attribution_delta(baseline_payload: dict[str, Any] | None, candidate_payload: dict[str, Any] | None) -> dict[str, Any]:
    if not baseline_payload or not candidate_payload:
        return {"warning": "Missing attribution payloads for delta."}

    return {
        "scorecard_delta": compare_attribution_scorecards(baseline_payload.get("scorecard"), candidate_payload.get("scorecard")),
        "signal_delta": compare_signal_contribution_delta(baseline_payload.get("signal_contributions"), candidate_payload.get("signal_contributions")),
        "cost_delta": compare_cost_attribution_delta(baseline_payload.get("cost_attributions"), candidate_payload.get("cost_attributions"))
    }

def compare_attribution_scorecards(baseline: dict[str, Any] | None, candidate: dict[str, Any] | None) -> dict[str, Any]:
    if not baseline or not candidate:
        return {}
    return {k: candidate.get(k, 0) - baseline.get(k, 0) for k in baseline.keys() if isinstance(baseline[k], (int, float))}

def compare_signal_contribution_delta(baseline: dict[str, Any] | None, candidate: dict[str, Any] | None) -> dict[str, Any]:
    return {}

def compare_cost_attribution_delta(baseline: dict[str, Any] | None, candidate: dict[str, Any] | None) -> dict[str, Any]:
    return {}

def attribution_delta_to_text(delta: dict[str, Any]) -> str:
    lines = ["--- ATTRIBUTION DELTA ---"]
    if "warning" in delta:
        lines.append(delta["warning"])
    else:
        lines.append(f"Scorecard Delta: {delta.get('scorecard_delta')}")
    return "\n".join(lines)
