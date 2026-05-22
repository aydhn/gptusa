from usa_signal_bot.paper_readiness_confirmation.reviewer_notes import (
    build_empty_reviewer_note,
    build_reviewer_note,
    validate_reviewer_note_safety
)

def test_build_empty_reviewer_note():
    n = build_empty_reviewer_note()
    assert n.note_text == ""
    assert n.requires_followup is False

def test_build_reviewer_note():
    n = build_reviewer_note("Looks good", "user1")
    assert n.note_text == "Looks good"
    assert n.reviewer_id == "user1"
    assert len(n.errors) == 0

def test_validate_reviewer_note_safety():
    n = build_reviewer_note("live approved", "user1")
    assert len(n.errors) == 1
    assert "live approved" in n.errors[0]
