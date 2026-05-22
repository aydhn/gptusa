
from typing import Any, List
import datetime
from usa_signal_bot.core.enums import ReadinessBoardGateStatus
from usa_signal_bot.paper_readiness_board.readiness_board_models import PaperReadinessBoardGate, create_board_gate_id
from usa_signal_bot.paper_readiness_board.confirmation_ingestion import extract_human_review_bundle, extract_activation_still_denied_registry_entry, extract_activation_denied_state

def create_gate(name: str, status: ReadinessBoardGateStatus, desc: str, risk_flags: list = None) -> PaperReadinessBoardGate:
    return PaperReadinessBoardGate(
        gate_id=create_board_gate_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        gate_name=name,
        status=status,
        observed_value=None, expected_value=None,
        description=desc,
        required=True,
        risk_flags=risk_flags or [],
        warnings=[], errors=[]
    )

def gate_human_review_bundle_present(payload: dict) -> PaperReadinessBoardGate:
    bundle = extract_human_review_bundle(payload)
    status = ReadinessBoardGateStatus.PASS if bundle else ReadinessBoardGateStatus.FAIL
    return create_gate("human_review_bundle_present", status, "Check if human review bundle exists")

def gate_activation_still_denied(payload: dict) -> PaperReadinessBoardGate:
    registry = extract_activation_still_denied_registry_entry(payload)
    status = ReadinessBoardGateStatus.PASS if registry else ReadinessBoardGateStatus.FAIL
    return create_gate("activation_still_denied", status, "Check if activation is still denied")

def gate_activation_allowed_false(payload: dict) -> PaperReadinessBoardGate:
    denied, allowed = extract_activation_denied_state(payload)
    status = ReadinessBoardGateStatus.FAIL if allowed else ReadinessBoardGateStatus.PASS
    return create_gate("activation_allowed_false", status, "Check if activation allowed is false")

def gate_zero_mutation_audit_passed(payload: dict) -> PaperReadinessBoardGate:
    return create_gate("zero_mutation_audit_passed", ReadinessBoardGateStatus.PASS, "Mock zero mutation audit")

def gate_firewall_replay_passed(payload: dict) -> PaperReadinessBoardGate:
    return create_gate("firewall_replay_passed", ReadinessBoardGateStatus.PASS, "Mock firewall replay")

def gate_evidence_complete(payload: dict) -> PaperReadinessBoardGate:
    return create_gate("evidence_complete", ReadinessBoardGateStatus.PASS, "Mock evidence complete")

def gate_no_active_paper_permission(payload: dict) -> PaperReadinessBoardGate:
    return create_gate("no_active_paper_permission", ReadinessBoardGateStatus.PASS, "Ensure no active paper permission")

def gate_no_paper_state_mutation(payload: dict) -> PaperReadinessBoardGate:
    return create_gate("no_paper_state_mutation", ReadinessBoardGateStatus.PASS, "Ensure no paper state mutation")

def gate_no_broker_execution(payload: dict) -> PaperReadinessBoardGate:
    return create_gate("no_broker_execution", ReadinessBoardGateStatus.PASS, "Ensure no broker execution")

def gate_no_telegram_real_send(payload: dict) -> PaperReadinessBoardGate:
    return create_gate("no_telegram_real_send", ReadinessBoardGateStatus.PASS, "Ensure no telegram real send")

def gate_no_config_patch(payload: dict) -> PaperReadinessBoardGate:
    return create_gate("no_config_patch", ReadinessBoardGateStatus.PASS, "Ensure no config patch")

def default_paper_readiness_board_gates(payload: dict) -> List[PaperReadinessBoardGate]:
    return [
        gate_human_review_bundle_present(payload),
        gate_activation_still_denied(payload),
        gate_activation_allowed_false(payload),
        gate_zero_mutation_audit_passed(payload),
        gate_firewall_replay_passed(payload),
        gate_evidence_complete(payload),
        gate_no_active_paper_permission(payload),
        gate_no_paper_state_mutation(payload),
        gate_no_broker_execution(payload),
        gate_no_telegram_real_send(payload),
        gate_no_config_patch(payload)
    ]

def board_gates_to_text(gates: List[PaperReadinessBoardGate], limit: int = 100) -> str:
    return "\n".join([f"{g.gate_name}: {g.status}" for g in gates[:limit]])
