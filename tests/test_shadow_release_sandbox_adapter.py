from usa_signal_bot.paper_shadow.release_sandbox_adapter import (
    shadow_context_from_release_sandbox_review, shadow_rehearsal_from_sandbox_review,
    attach_shadow_metadata_to_sandbox_review, release_sandbox_shadow_summary
)

def test_shadow_context_from_release_sandbox_review():
    ctx = shadow_context_from_release_sandbox_review({"sandbox_id": "sbx1"})
    assert ctx.source_sandbox_id == "sbx1"

def test_shadow_rehearsal_from_sandbox_review():
    session = shadow_rehearsal_from_sandbox_review({"sandbox_id": "sbx1"})
    assert session.status == "COMPLETED"

def test_attach_shadow_metadata_to_sandbox_review():
    session = shadow_rehearsal_from_sandbox_review({"sandbox_id": "sbx1"})
    payload = attach_shadow_metadata_to_sandbox_review({"sandbox_id": "sbx1"}, session)
    assert "shadow_rehearsal_metadata" in payload
    assert payload["shadow_rehearsal_metadata"]["status"] == "COMPLETED"
