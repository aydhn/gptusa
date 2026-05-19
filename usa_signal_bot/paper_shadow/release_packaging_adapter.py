from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import ShadowSimulationContext, ShadowRehearsalSession
from usa_signal_bot.paper_shadow.simulation_context import build_shadow_simulation_context_from_sandbox_payload

def shadow_context_from_bundle_payload(bundle_payload: dict[str, Any]) -> ShadowSimulationContext:
    # Bundle payload might not have review_id, adapt accordingly
    payload_adapted = bundle_payload.copy()
    if "bundle_id" not in payload_adapted:
        payload_adapted["bundle_id"] = bundle_payload.get("id")
    return build_shadow_simulation_context_from_sandbox_payload(payload_adapted)

def shadow_rehearsal_from_bundle_payload(bundle_payload: dict[str, Any]) -> ShadowRehearsalSession:
    from usa_signal_bot.paper_shadow.rehearsal_runner import PaperShadowRehearsalRunner
    context = shadow_context_from_bundle_payload(bundle_payload)
    runner = PaperShadowRehearsalRunner()
    return runner.run_rehearsal(context)

def attach_shadow_metadata_to_bundle_payload(bundle_payload: dict[str, Any], session: ShadowRehearsalSession) -> dict[str, Any]:
    bundle_payload["shadow_rehearsal_id"] = session.session_id
    bundle_payload["shadow_status"] = session.status.value
    return bundle_payload

def release_packaging_shadow_summary(bundle_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "bundle_id": bundle_payload.get("bundle_id", bundle_payload.get("id")),
        "shadow_rehearsal_id": bundle_payload.get("shadow_rehearsal_id"),
        "shadow_status": bundle_payload.get("shadow_status")
    }

def release_packaging_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = release_packaging_shadow_summary(payload)
    text = "Release Packaging Adapter Summary\n"
    for k, v in summary.items():
         text += f"{k}: {v}\n"
    return text
