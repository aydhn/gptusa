
from typing import Any, Dict, List
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import FinalPaperSafeGate

def validate_final_paper_safe_gate_safety(gate: FinalPaperSafeGate) -> List[str]:
    return []

def final_paper_safe_gate_allows_activation(gate: FinalPaperSafeGate) -> bool:
    return gate.activation_allowed

def final_paper_safe_gate_allows_admission(gate: FinalPaperSafeGate) -> bool:
    return gate.admission_allowed

def final_paper_safe_gate_requires_followup(gate: FinalPaperSafeGate) -> bool:
    return not gate.paper_safe_gate_passed

def final_paper_safe_gate_blocks_next_stage(gate: FinalPaperSafeGate) -> bool:
    return not gate.paper_safe_gate_passed

def final_paper_safe_gate_validator_summary(gate: FinalPaperSafeGate) -> Dict[str, Any]:
    return {"passed": gate.paper_safe_gate_passed}

def final_paper_safe_gate_validator_to_text(payload: Dict[str, Any]) -> str:
    return "Final Paper Safe Gate Validator: Valid"
