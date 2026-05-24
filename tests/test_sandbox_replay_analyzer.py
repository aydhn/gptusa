import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_analyzer import analyze_sandbox_runtime_admission_replay_result
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_engine import SandboxRuntimeAdmissionBlockerReplayEngine
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_plan import build_default_sandbox_runtime_admission_replay_plan

def test_analyze_sandbox_replay():
    plan = build_default_sandbox_runtime_admission_replay_plan()
    events = [{"attempt_type": t, "blocked": True} for t in plan.required_attempt_types]
    events[0]["blocked"] = False
    engine = SandboxRuntimeAdmissionBlockerReplayEngine()
    result = engine.replay(plan, events)

    analysis = analyze_sandbox_runtime_admission_replay_result(result)
    assert analysis["passed"] is False
    assert analysis["requires_followup"] is True
    assert len(analysis["followups"]) > 0
