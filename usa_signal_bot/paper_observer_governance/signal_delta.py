from typing import Any
from usa_signal_bot.core.enums import ObserverGovernanceRiskFlag

def calculate_signal_delta(paper_snapshot: dict[str, Any], observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {"counts": compare_signal_counts(paper_snapshot, observer_payload), "symbols": compare_signal_symbols(paper_snapshot, observer_payload)}

def compare_signal_counts(paper_snapshot: dict[str, Any], observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {"paper": paper_snapshot.get("signal_count", 0), "observer": observer_payload.get("signal_count", 0)}

def compare_signal_symbols(paper_snapshot: dict[str, Any], observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {"paper": [], "observer": []}

def signal_delta_risk_flags(delta: dict[str, Any]) -> list[ObserverGovernanceRiskFlag]:
    return []

def signal_delta_to_text(delta: dict[str, Any]) -> str:
    return str(delta)
