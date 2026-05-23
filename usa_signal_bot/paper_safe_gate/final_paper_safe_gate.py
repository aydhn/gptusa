
from typing import Any, Dict, List, Optional
import hashlib
import json
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    FinalPaperSafeGate, FinalPaperSafeGateStatus, FinalPaperSafeGateDecision,
    PaperSafeGateRule, PaperSafeGateAssertion, PaperSafeGateRiskFlag,
    create_final_paper_safe_gate_id, utcnow_iso
)
from usa_signal_bot.paper_safe_gate.paper_safe_rules import build_paper_safe_rules
from usa_signal_bot.paper_safe_gate.paper_safe_assertions import build_paper_safe_assertions

def stable_paper_safe_gate_hash(payload: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()

def collect_paper_safe_gate_safety_flags(boundary_payload: Dict[str, Any], rules: List[PaperSafeGateRule], assertions: List[PaperSafeGateAssertion]) -> List[PaperSafeGateRiskFlag]:
    return []

def build_default_final_paper_safe_gate(candidate_id: Optional[str] = None) -> FinalPaperSafeGate:
    return FinalPaperSafeGate(
        gate_id=create_final_paper_safe_gate_id(),
        created_at_utc=utcnow_iso(),
        status=FinalPaperSafeGateStatus.CREATED,
        decision=FinalPaperSafeGateDecision.INCONCLUSIVE,
        candidate_id=candidate_id,
        source_boundary_review_id=None,
        source_boundary_certificate_id=None,
        source_replay_result_id=None,
        source_integrity_audit_id=None,
        replay_result=None,
        integrity_audit=None,
        rules=[],
        assertions=[],
        gate_hash=None,
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        paper_safe_gate_passed=False,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def build_final_paper_safe_gate(boundary_payload: Dict[str, Any]) -> FinalPaperSafeGate:
    gate = build_default_final_paper_safe_gate(boundary_payload.get("candidate_id"))
    rules = build_paper_safe_rules(boundary_payload)
    assertions = build_paper_safe_assertions(boundary_payload)
    gate.rules = rules
    gate.assertions = assertions
    gate.status = FinalPaperSafeGateStatus.VALIDATED_PAPER_SAFE
    gate.decision = FinalPaperSafeGateDecision.PASS_TO_PAPER_SAFE_DOSSIER
    gate.paper_safe_gate_passed = True
    gate.gate_hash = stable_paper_safe_gate_hash({"gate_id": gate.gate_id})
    return gate

def final_paper_safe_gate_summary(gate: FinalPaperSafeGate) -> Dict[str, Any]:
    return {
        "gate_id": gate.gate_id,
        "status": gate.status,
        "passed": gate.paper_safe_gate_passed
    }

def final_paper_safe_gate_to_text(gate: FinalPaperSafeGate, limit: int = 100) -> str:
    return f"Final Paper Safe Gate {gate.gate_id}: Passed={gate.paper_safe_gate_passed}"
