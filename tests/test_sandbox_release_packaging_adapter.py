import pytest
from usa_signal_bot.release_sandbox.release_packaging_adapter import (
    sandbox_activation_from_versioned_bundle_payload,
    sandbox_preview_from_release_packaging_review,
    attach_sandbox_metadata_to_bundle_payload,
    release_packaging_adapter_to_text
)

def test_release_packaging_adapter():
    bundle_payload = {"manifest": {"bundle_id": "b1"}}
    plan = sandbox_activation_from_versioned_bundle_payload(bundle_payload)
    assert plan.bundle_id == "b1"

    packaging_payload = {"bundle": bundle_payload}
    review = sandbox_preview_from_release_packaging_review(packaging_payload)
    assert len(review.activation_plans) == 1

    mod_bundle = attach_sandbox_metadata_to_bundle_payload(bundle_payload, review)
    assert "sandbox_review_id" in mod_bundle

    txt = release_packaging_adapter_to_text(packaging_payload)
    assert "Sandbox Review present" in txt
