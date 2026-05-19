import pytest
from usa_signal_bot.paper_shadow.release_packaging_adapter import (
    shadow_context_from_bundle_payload,
    release_packaging_adapter_to_text
)

def test_shadow_release_packaging_adapter():
    payload = {"id": "test_bundle"}
    ctx = shadow_context_from_bundle_payload(payload)
    assert ctx.source_bundle_id == "test_bundle"

    text = release_packaging_adapter_to_text(payload)
    assert "Release Packaging Adapter Summary" in text
