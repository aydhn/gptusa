import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    SandboxRuntimeAdmissionReplayPlan,
    SandboxRuntimeAdmissionReplayResult,
    SandboxRuntimeAdmissionReplayItem,
    create_sandbox_replay_plan_id
)
from usa_signal_bot.core.enums import SandboxRuntimeAdmissionReplayStatus, SandboxRuntimeAdmissionReplayOutcome

def test_sandbox_replay_plan_model():
    plan = SandboxRuntimeAdmissionReplayPlan(
        replay_plan_id=create_sandbox_replay_plan_id(),
        created_at_utc="2023-01-01T00:00:00Z",
        candidate_id="cand-1",
        source_simulator_dossier_id=None,
        source_acceptance_seal_id=None,
        required_attempt_types=[],
        require_all_attempts_blocked=True,
        execution_enabled=False,
        sandbox_runtime_admission_enabled=False,
        paper_sandbox_runtime_enabled=False,
        simulator_admission_enabled=False,
        local_paper_simulator_enabled=False,
        active_paper_enabled=False,
        paper_admission_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )
    assert plan.candidate_id == "cand-1"
    assert plan.require_all_attempts_blocked is True
