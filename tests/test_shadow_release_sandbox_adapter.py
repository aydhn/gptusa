import pytest
from usa_signal_bot.paper_shadow.release_sandbox_adapter import (
    shadow_context_from_release_sandbox_review,
    release_sandbox_adapter_to_text
)

def test_shadow_release_sandbox_adapter():
    payload = {"review_id": "test_sandbox", "bundle_id": "b1"}
    ctx = shadow_context_from_release_sandbox_review(payload)
    assert ctx.source_sandbox_id == "test_sandbox"

    text = release_sandbox_adapter_to_text(payload)
    assert "Release Sandbox Adapter Summary" in text
