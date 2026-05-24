import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_plan import build_default_sandbox_runtime_admission_replay_plan

def test_build_sandbox_replay_plan():
    plan = build_default_sandbox_runtime_admission_replay_plan()
    assert plan.require_all_attempts_blocked is True
    assert plan.execution_enabled is False
    assert "START_PAPER_SANDBOX_RUNTIME" in plan.required_attempt_types
