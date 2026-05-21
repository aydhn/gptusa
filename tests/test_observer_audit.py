from usa_signal_bot.paper_observer.observer_audit import (
    create_observer_audit_entry,
    audit_entry_from_observer_enrollment,
    audit_entry_from_observer_session
)
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context
from usa_signal_bot.paper_observer.parallel_monitor import run_read_only_parallel_monitor

def test_create_observer_audit_entry():
    entry = create_observer_audit_entry("Entity", "123", "ACTION", "Rationale")
    assert entry.entity_type == "Entity"
    assert entry.action == "ACTION"

def test_audit_entry_from_observer_enrollment():
    enrollment = build_observer_enrollment("cand_1", "ticket_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    entry = audit_entry_from_observer_enrollment(enrollment)
    assert entry.action == "ENROLLMENT_CREATED"
    assert "cand_1" in entry.rationale

def test_audit_entry_from_observer_session():
    context = build_mock_observer_runtime_context()
    session = run_read_only_parallel_monitor(context)
    entry = audit_entry_from_observer_session(session)
    assert entry.action == "SESSION_COMPLETED"
