import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_engine import SandboxRuntimeAdmissionBlockerReplayEngine
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_plan import build_default_sandbox_runtime_admission_replay_plan
from usa_signal_bot.core.enums import SandboxRuntimeAdmissionReplayOutcome

def test_sandbox_replay_engine_pass():
    plan = build_default_sandbox_runtime_admission_replay_plan()
    events = [{"attempt_type": t, "blocked": True} for t in plan.required_attempt_types]
    engine = SandboxRuntimeAdmissionBlockerReplayEngine()
    result = engine.replay(plan, events)
    assert result.passed is True
    assert result.outcome == SandboxRuntimeAdmissionReplayOutcome.ALL_SANDBOX_RUNTIME_ADMISSION_ATTEMPTS_BLOCKED
    assert result.allowed_attempt_count == 0

def test_sandbox_replay_engine_fail():
    plan = build_default_sandbox_runtime_admission_replay_plan()
    events = [{"attempt_type": t, "blocked": True} for t in plan.required_attempt_types]
    events[0]["blocked"] = False # Unblocked attempt
    engine = SandboxRuntimeAdmissionBlockerReplayEngine()
    result = engine.replay(plan, events)
    assert result.passed is False
    assert result.outcome == SandboxRuntimeAdmissionReplayOutcome.SANDBOX_RUNTIME_ADMISSION_ATTEMPT_ALLOWED
    assert result.allowed_attempt_count == 1
