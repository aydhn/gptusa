import pytest
from usa_signal_bot.paper_readiness_board.readiness_board_models import (
    PaperReadinessBoardGate, WriteBlockedRuntimeAdapterProof, RuntimeWriteBlockEvent,
    ActivationFirewallRule, ActivationFirewallEvent, PaperReadinessBoardReview, PaperReadinessBoardFullReview,
    create_board_gate_id, validate_write_blocked_runtime_adapter_proof, validate_paper_readiness_board_review
)
from usa_signal_bot.core.enums import ReadinessBoardGateStatus, WriteBlockedAdapterStatus, RuntimeWriteAttemptType, WriteBlockAction, ActivationAttemptType, ActivationFirewallStatus, ActivationFirewallDecision, PaperReadinessBoardDecision, PaperReadinessBoardStatus

def test_models():
    assert create_board_gate_id() is not None

    proof = WriteBlockedRuntimeAdapterProof(
        proof_id="test", created_at_utc="test", status=WriteBlockedAdapterStatus.PROOF_CREATED,
        candidate_id=None, read_only_snapshot_hash=None, write_attempt_types_tested=[],
        blocked_write_attempt_count=1, unblocked_write_attempt_count=0,
        all_writes_blocked=True, allows_active_paper=False, allows_broker_execution=False,
        allows_paper_state_mutation=False, allows_config_patch=False, allows_telegram_real_send=False,
        risk_flags=[], warnings=[], errors=[]
    )
    validate_write_blocked_runtime_adapter_proof(proof)

    review = PaperReadinessBoardReview(
        board_review_id="test", created_at_utc="test", status=PaperReadinessBoardStatus.PASSED_WITH_ACTIVATION_DENIED,
        decision=PaperReadinessBoardDecision.PASS_WITH_ACTIVATION_DENIED, candidate_id=None,
        source_confirmation_review_id=None, source_human_review_bundle_id=None, source_activation_denied_registry_id=None,
        gates=[], write_block_proofs=[], activation_firewall_events=[], readiness_confidence=None, evidence_refs=[],
        required_followups=[], safety_flags=[], manual_review_required=True, activation_denied=True, activation_allowed=False,
        allows_active_paper=False, allows_broker_execution=False, allows_paper_state_mutation=False, allows_config_patch=False,
        allows_telegram_real_send=False, warnings=[], errors=[]
    )
    validate_paper_readiness_board_review(review)

from usa_signal_bot.paper_readiness_board.confirmation_ingestion import ingest_readiness_confirmation_review, extract_activation_denied_state
def test_ingestion():
    payload = {"activation_denied": True, "activation_allowed": False}
    assert extract_activation_denied_state(payload) == (True, False)

from usa_signal_bot.paper_readiness_board.eligibility_checker import evaluate_paper_readiness_board_eligibility
def test_eligibility():
    assert evaluate_paper_readiness_board_eligibility({"activation_allowed": True}) == PaperReadinessBoardDecision.BLOCK

from usa_signal_bot.paper_readiness_board.board_gates import default_paper_readiness_board_gates
def test_gates():
    gates = default_paper_readiness_board_gates({})
    assert len(gates) > 0

from usa_signal_bot.paper_readiness_board.board_decision import PaperReadinessBoardDecisionEngine
def test_decision():
    engine = PaperReadinessBoardDecisionEngine()
    review = engine.decide({"activation_allowed": True}, [])
    assert review.status == PaperReadinessBoardStatus.BLOCKED

from usa_signal_bot.paper_readiness_board.runtime_write_detector import detect_runtime_write_attempts_in_text
def test_write_detector():
    attempts = detect_runtime_write_attempts_in_text("paper'a uygula ve emir gönder")
    assert RuntimeWriteAttemptType.PAPER_STATE_WRITE in attempts
    assert RuntimeWriteAttemptType.BROKER_SEND in attempts

from usa_signal_bot.paper_readiness_board.write_blocked_adapter import WriteBlockedPaperRuntimeAdapter
def test_adapter():
    adapter = WriteBlockedPaperRuntimeAdapter()
    event = adapter.attempt_paper_order_create()
    assert event.blocked is True

from usa_signal_bot.paper_readiness_board.activation_firewall import FinalActivationFirewall, simulate_activation_attempts
def test_firewall():
    fw = FinalActivationFirewall()
    event = fw.evaluate_attempt(ActivationAttemptType.ENABLE_ACTIVE_PAPER)
    assert event.blocked is True
    assert event.activation_allowed is False

from usa_signal_bot.paper_readiness_board.board_safety_validator import validate_board_safety
def test_safety():
    assert validate_board_safety() == []

from usa_signal_bot.paper_readiness_board.board_audit import create_paper_readiness_board_audit_entry
def test_audit():
    entry = create_paper_readiness_board_audit_entry("Test", "123", "ACTION", "Rationale")
    assert entry.action == "ACTION"
