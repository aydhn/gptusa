from typing import Any
from usa_signal_bot.core.enums import ObserverGovernanceRiskFlag

def calculate_proposal_delta(paper_snapshot: dict[str, Any], observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {"counts": compare_proposal_counts(paper_snapshot, observer_payload), "symbols": compare_proposal_symbols(paper_snapshot, observer_payload)}

def compare_proposal_counts(paper_snapshot: dict[str, Any], observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {"paper": paper_snapshot.get("proposal_count", 0), "observer": observer_payload.get("proposal_count", 0)}

def compare_proposal_symbols(paper_snapshot: dict[str, Any], observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {"paper": [], "observer": []}

def proposal_delta_risk_flags(delta: dict[str, Any]) -> list[ObserverGovernanceRiskFlag]:
    return []

def proposal_delta_to_text(delta: dict[str, Any]) -> str:
    return str(delta)
