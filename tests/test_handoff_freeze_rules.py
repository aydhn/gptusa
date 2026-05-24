import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_rules import build_handoff_freeze_rules
from usa_signal_bot.core.enums import HandoffFreezeRuleStatus

def test_build_handoff_freeze_rules():
    payload = {
        "sandbox_runtime_admission_allowed": False,
        "mutation_detected": False,
        "simulator_acceptance_seal": {"status": "VALIDATED"}
    }
    rules = build_handoff_freeze_rules(payload)
    for rule in rules:
        if rule.rule_name in ["sandbox_runtime_admission_allowed_false", "mutation_detected_false", "simulator_acceptance_seal_valid", "sandbox_runtime_admission_replay_passed", "simulator_evidence_freeze_valid"]:
            continue
        assert rule.status == HandoffFreezeRuleStatus.PASS
