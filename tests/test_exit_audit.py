from usa_signal_bot.paper_observation.observation_models import QuarantineExitReview, QuarantineExitDecision
from usa_signal_bot.paper_observation.exit_audit import create_observation_audit_entry, audit_entry_from_exit_review, append_observation_audit_entry, observation_audit_summary, observation_audit_to_text

def test_exit_audit():
    entry = create_observation_audit_entry("Entity", "id1", "ACTION", "Rationale")
    assert entry.entity_id == "id1"

    rev = QuarantineExitReview("r1", "2023", "w1", "c1", "t1", QuarantineExitDecision.KEEP_IN_QUARANTINE, None, None, [], [], "Rationale", [], False)
    audit = audit_entry_from_exit_review(rev)
    assert audit.action == "QUARANTINE_EXIT_DECISION"
    assert audit.decision == "KEEP_IN_QUARANTINE"

    entries = append_observation_audit_entry([entry], audit)
    assert len(entries) == 2

    summ = observation_audit_summary(entries)
    assert summ["total_entries"] == 2

    text = observation_audit_to_text(entries)
    assert "Total Entries: 2" in text
