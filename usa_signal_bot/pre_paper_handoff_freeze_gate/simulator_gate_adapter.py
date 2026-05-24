from typing import Any, Tuple, List
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import PrePaperHandoffFreezeFullReview

def handoff_freeze_evidence_from_simulator_gate(payload: dict[str, Any]) -> List[str]:
    # Returns relevant evidence keys
    return []

def simulator_gate_supports_handoff_freeze(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    if payload.get("simulator_admission_allowed", False):
        warnings.append("Simulator gate admits paper simulator")
    return len(warnings) == 0, warnings

def attach_handoff_freeze_hint_to_simulator_gate_payload(payload: dict[str, Any], review: PrePaperHandoffFreezeFullReview) -> dict[str, Any]:
    res = dict(payload)
    res["pre_paper_handoff_freeze_hint"] = {
        "review_id": review.review_id,
        "frozen": True
    }
    return res

def simulator_gate_handoff_freeze_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("pre_paper_handoff_freeze_hint", {})

def simulator_gate_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Simulator Gate Adapter: {simulator_gate_handoff_freeze_summary(payload)}"
