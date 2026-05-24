import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.eligibility_checker import evaluate_handoff_freeze_gate_eligibility
from usa_signal_bot.core.enums import PrePaperHandoffFreezeGateDecision

def test_eligibility_checker_valid():
    payload = {
        "simulator_dossier": {"decision": "CREATE_SIMULATOR_DOSSIER"},
        "simulator_acceptance_seal": {"status": "VALIDATED"},
        "sandbox_runtime_admission_blocker_events": [{"blocked": True, "attempt_type": "START_PAPER_SANDBOX_RUNTIME"}],
        "sandbox_runtime_admission_allowed": False
    }
    decision = evaluate_handoff_freeze_gate_eligibility(payload)
    assert decision == PrePaperHandoffFreezeGateDecision.COMPLETE_PRE_PAPER_HANDOFF_FREEZE

def test_eligibility_checker_reject():
    payload = {}
    decision = evaluate_handoff_freeze_gate_eligibility(payload)
    assert decision == PrePaperHandoffFreezeGateDecision.REJECT
