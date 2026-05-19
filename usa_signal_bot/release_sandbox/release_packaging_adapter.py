from typing import Any, Dict
from usa_signal_bot.release_sandbox.sandbox_models import SandboxActivationPlan, ReleaseSandboxReview
from usa_signal_bot.release_sandbox.activation_planner import build_sandbox_activation_plan
from usa_signal_bot.release_sandbox.sandbox_report import build_sandbox_review

def sandbox_activation_from_versioned_bundle_payload(bundle_payload: Dict[str, Any]) -> SandboxActivationPlan:
    return build_sandbox_activation_plan(bundle_payload)

def sandbox_preview_from_release_packaging_review(packaging_payload: Dict[str, Any]) -> ReleaseSandboxReview:
    bundle_payload = packaging_payload.get("bundle", {})
    activation_plan = sandbox_activation_from_versioned_bundle_payload(bundle_payload)
    return build_sandbox_review(activation_plan)

def attach_sandbox_metadata_to_bundle_payload(bundle_payload: Dict[str, Any], review: ReleaseSandboxReview) -> Dict[str, Any]:
    bundle_payload["sandbox_review_id"] = review.review_id
    bundle_payload["sandbox_activation_status"] = review.activation_plans[0].status.value if review.activation_plans else "UNKNOWN"
    return bundle_payload

def release_packaging_sandbox_summary(packaging_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "has_sandbox_review": "sandbox_review_id" in packaging_payload.get("bundle", {})
    }

def release_packaging_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = release_packaging_sandbox_summary(payload)
    return f"Release Packaging Adapter: Sandbox Review present = {summary['has_sandbox_review']}"
