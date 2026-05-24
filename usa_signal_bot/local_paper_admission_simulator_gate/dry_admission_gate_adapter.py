from typing import Any
from .simulator_gate_models import SimulatorGateFullReview

def simulator_evidence_from_dry_admission_gate(payload: dict[str, Any]) -> list[str]:
    return []

def dry_admission_gate_supports_simulator_gate(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return False, []

def attach_simulator_hint_to_dry_admission_gate_payload(payload: dict[str, Any], review: SimulatorGateFullReview) -> dict[str, Any]:
    return payload

def dry_admission_gate_simulator_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def dry_admission_gate_adapter_to_text(payload: dict[str, Any]) -> str:
    return ""
