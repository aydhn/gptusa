import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_assertions import build_handoff_freeze_assertions
from usa_signal_bot.core.enums import HandoffFreezeAssertionStatus

def test_build_handoff_freeze_assertions():
    payload = {
        "sandbox_runtime_admission_allowed": False,
        "mutation_detected": False,
        "allows_broker_execution": False,
        "pre_paper_handoff_complete": True
    }
    assertions = build_handoff_freeze_assertions(payload)
    for assertion in assertions:
        assert assertion.status == HandoffFreezeAssertionStatus.PASS
