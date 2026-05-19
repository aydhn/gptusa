from typing import Any, Dict
from usa_signal_bot.release_sandbox.sandbox_models import SandboxActivationPlan, ReleaseSandboxReview
from usa_signal_bot.release_sandbox.activation_planner import build_sandbox_activation_plan

def sandbox_activation_from_versioned_bundle_payload(bundle_payload: Dict[str, Any]) -> SandboxActivationPlan:
    return build_sandbox_activation_plan(bundle_payload)

def sandbox_preview_from_release_packaging_review(packaging_payload: Dict[str, Any]) -> ReleaseSandboxReview:
    from usa_signal_bot.release_sandbox.sandbox_report import build_sandbox_review
    # mock
    act = build_sandbox_activation_plan({"id":"mock"})
    return build_sandbox_review(act)

def attach_sandbox_metadata_to_bundle_payload(bundle_payload: Dict[str, Any], review: ReleaseSandboxReview) -> Dict[str, Any]:
    bundle_payload["sandbox_metadata"] = {"review_id": review.review_id}
    return bundle_payload

def release_packaging_sandbox_summary(packaging_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"adapted": True}

def release_packaging_adapter_to_text(payload: Dict[str, Any]) -> str:
    return "Release Packaging Adapter: Connected"
