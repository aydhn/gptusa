import pytest
from usa_signal_bot.runtime_lifecycle.lifecycle_state_machine import RuntimeLifecycleStateMachine
from usa_signal_bot.core.enums import RuntimeLifecycleStatus, LifecycleTransitionStatus

def test_state_machine_valid_transitions():
    sm = RuntimeLifecycleStateMachine()
    assert sm.current_status() == RuntimeLifecycleStatus.DRAFT

    t1 = sm.transition(RuntimeLifecycleStatus.CREATED, "Init")
    assert t1.transition_status == LifecycleTransitionStatus.ALLOWED_METADATA_ONLY
    assert sm.current_status() == RuntimeLifecycleStatus.CREATED

    t2 = sm.transition(RuntimeLifecycleStatus.CONFIG_CHECKED, "Config ok")
    assert t2.transition_status == LifecycleTransitionStatus.ALLOWED_METADATA_ONLY
    assert sm.current_status() == RuntimeLifecycleStatus.CONFIG_CHECKED

def test_state_machine_blocks_unsafe_transitions():
    sm = RuntimeLifecycleStateMachine()
    assert sm.current_status() == RuntimeLifecycleStatus.DRAFT

    # Trying to skip states
    t = sm.transition(RuntimeLifecycleStatus.READINESS_CHECKED, "Skipping")
    assert t.transition_status == LifecycleTransitionStatus.BLOCKED
    assert sm.current_status() == RuntimeLifecycleStatus.BLOCKED

def test_state_machine_allows_abort():
    sm = RuntimeLifecycleStateMachine(RuntimeLifecycleStatus.CONFIG_CHECKED)
    t = sm.transition(RuntimeLifecycleStatus.FAILED, "Abort")
    assert t.transition_status == LifecycleTransitionStatus.ALLOWED_METADATA_ONLY
    assert sm.current_status() == RuntimeLifecycleStatus.FAILED
