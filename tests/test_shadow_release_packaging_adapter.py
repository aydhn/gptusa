from usa_signal_bot.paper_shadow.release_packaging_adapter import (
    shadow_context_from_bundle_payload, shadow_rehearsal_from_bundle_payload,
    attach_shadow_metadata_to_bundle_payload
)

def test_shadow_context_from_bundle_payload():
    ctx = shadow_context_from_bundle_payload({"bundle_id": "bndl1"})
    assert ctx.source_bundle_id == "bndl1"

def test_shadow_rehearsal_from_bundle_payload():
    session = shadow_rehearsal_from_bundle_payload({"bundle_id": "bndl1"})
    assert session.status == "COMPLETED"
