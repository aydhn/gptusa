
from usa_signal_bot.paper_no_write_transition.transition_audit import create_no_write_transition_audit_entry, NoWriteTransitionAuditEntryParams
def test_audit():
    params = NoWriteTransitionAuditEntryParams(
        entity_type="test",
        entity_id="id",
        action="action",
        rationale="rationale"
    )
    assert create_no_write_transition_audit_entry(params) is not None
