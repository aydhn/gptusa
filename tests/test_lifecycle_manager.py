import pytest
from usa_signal_bot.runtime_lifecycle.lifecycle_manager import RuntimeLifecycleManager
from usa_signal_bot.runtime_lifecycle.lifecycle_report import build_runtime_lifecycle_full_review
from usa_signal_bot.core.enums import RuntimeLifecycleStatus, ReadinessGateDecision, RuntimeLifecycleDecision

def test_lifecycle_manager_dry_run():
    manager = RuntimeLifecycleManager()
    ctx = manager.run_lifecycle_dry_run()

    assert ctx.status == RuntimeLifecycleStatus.READY_FOR_FUTURE_PHASE
    assert ctx.decision == RuntimeLifecycleDecision.READY_FOR_PHASE105_REVIEW
    assert ctx.ready_for_phase105 is True
    assert ctx.activation_allowed is False
    assert ctx.broker_execution_enabled is False

def test_lifecycle_full_review_generation():
    review = build_runtime_lifecycle_full_review()
    assert review.lifecycle_context is not None
    assert review.readiness_gate is not None
    assert review.startup_report is not None
    assert review.readiness_gate.decision == ReadinessGateDecision.PASS_TO_PHASE105_CORE_ACCEPTANCE
