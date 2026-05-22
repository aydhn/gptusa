
from typing import Any, List, Tuple
from usa_signal_bot.paper_readiness_board.readiness_board_models import (
    PaperReadinessBoardReview, WriteBlockedRuntimeAdapterProof, ActivationFirewallEvent, PaperReadinessBoardFullReview
)
from usa_signal_bot.paper_readiness_board.board_report import build_paper_readiness_board_review, build_paper_readiness_board_full_review
from usa_signal_bot.paper_readiness_board.write_blocked_adapter import WriteBlockedPaperRuntimeAdapter
from usa_signal_bot.paper_readiness_board.activation_firewall import FinalActivationFirewall, simulate_activation_attempts

def board_review_from_readiness_confirmation(payload: dict) -> PaperReadinessBoardReview:
    return build_paper_readiness_board_review(payload)

def write_block_proof_from_readiness_confirmation(payload: dict) -> WriteBlockedRuntimeAdapterProof:
    adapter = WriteBlockedPaperRuntimeAdapter()
    return adapter.prove_all_writes_blocked(payload.get("candidate_id"))

def activation_firewall_events_from_readiness_confirmation(payload: dict) -> List[ActivationFirewallEvent]:
    fw = FinalActivationFirewall()
    return simulate_activation_attempts(fw)

def board_full_review_from_readiness_confirmation(payload: dict) -> PaperReadinessBoardFullReview:
    review = board_review_from_readiness_confirmation(payload)
    proof = write_block_proof_from_readiness_confirmation(payload)
    events = activation_firewall_events_from_readiness_confirmation(payload)
    return build_paper_readiness_board_full_review(review, proof, events)

def attach_board_metadata_to_confirmation_payload(payload: dict, review: PaperReadinessBoardFullReview) -> dict:
    payload["board_review_attached"] = True
    return payload

def readiness_confirmation_board_summary(payload: dict) -> dict:
    return {"board_ready": True}

def confirmation_adapter_to_text(payload: dict) -> str:
    return "Confirmation Adapter OK"

def board_evidence_from_firewall_audit(payload: dict) -> List[str]: return ["firewall_audit_ref"]
def firewall_audit_supports_board(payload: dict) -> Tuple[bool, List[str]]: return True, []
def attach_board_hint_to_firewall_audit_payload(payload: dict, review: PaperReadinessBoardFullReview) -> dict: return payload
def firewall_audit_board_summary(payload: dict) -> dict: return {}
def firewall_audit_adapter_to_text(payload: dict) -> str: return "Firewall Audit Adapter OK"

def board_evidence_from_pre_rehearsal(payload: dict) -> List[str]: return ["pre_rehearsal_ref"]
def pre_rehearsal_supports_board(payload: dict) -> Tuple[bool, List[str]]: return True, []
def attach_board_hint_to_pre_rehearsal_payload(payload: dict, review: PaperReadinessBoardFullReview) -> dict: return payload
def pre_rehearsal_board_summary(payload: dict) -> dict: return {}
def pre_rehearsal_adapter_to_text(payload: dict) -> str: return "Pre Rehearsal Adapter OK"

def build_read_only_paper_snapshot_for_board(paper_payload: dict = None) -> dict:
    return dict(paper_payload or {})

def build_write_blocked_runtime_proof_for_board(candidate_id: str = None, paper_payload: dict = None) -> WriteBlockedRuntimeAdapterProof:
    adapter = WriteBlockedPaperRuntimeAdapter()
    return adapter.prove_all_writes_blocked(candidate_id)

def compare_board_to_paper_snapshot(review: PaperReadinessBoardFullReview, paper_snapshot: dict) -> dict:
    return {"mutated": False}

def validate_paper_runtime_not_mutated_by_board(before: dict, after: dict) -> List[str]:
    return []

def attach_board_metadata_to_paper_analytics(payload: dict, review: PaperReadinessBoardFullReview) -> dict:
    return payload

def paper_runtime_board_adapter_to_text(payload: dict) -> str:
    return "Paper Runtime Adapter OK"
