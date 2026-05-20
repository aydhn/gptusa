from typing import Any, Dict
from usa_signal_bot.paper_shadow.shadow_models import ShadowSimulationContext, ShadowRehearsalSession
from usa_signal_bot.paper_shadow.simulation_context import build_shadow_simulation_context_from_sandbox_payload
from usa_signal_bot.paper_shadow.rehearsal_runner import PaperShadowRehearsalRunner

def shadow_context_from_bundle_payload(bundle_payload: Dict[str, Any]) -> ShadowSimulationContext:
    return build_shadow_simulation_context_from_sandbox_payload({"bundle_id": bundle_payload.get("bundle_id")})

def shadow_rehearsal_from_bundle_payload(bundle_payload: Dict[str, Any]) -> ShadowRehearsalSession:
    context = shadow_context_from_bundle_payload(bundle_payload)
    runner = PaperShadowRehearsalRunner()
    return runner.run_rehearsal(context)

def attach_shadow_metadata_to_bundle_payload(bundle_payload: Dict[str, Any], session: ShadowRehearsalSession) -> Dict[str, Any]:
    bundle_payload["shadow_rehearsal_metadata"] = {
        "session_id": session.session_id,
        "status": session.status.value,
        "safety_safe": len(session.safety_flags) == 0
    }
    return bundle_payload

def release_packaging_shadow_summary(bundle_payload: Dict[str, Any]) -> Dict[str, Any]:
    return bundle_payload.get("shadow_rehearsal_metadata", {})

def release_packaging_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"BundleShadowMetadata({payload})"
