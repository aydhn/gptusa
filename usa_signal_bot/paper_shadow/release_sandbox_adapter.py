from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import ShadowSimulationContext, ShadowRehearsalSession
from usa_signal_bot.paper_shadow.simulation_context import build_shadow_simulation_context_from_sandbox_payload

def shadow_context_from_release_sandbox_review(sandbox_payload: dict[str, Any]) -> ShadowSimulationContext:
    return build_shadow_simulation_context_from_sandbox_payload(sandbox_payload)

def shadow_rehearsal_from_sandbox_review(sandbox_payload: dict[str, Any]) -> ShadowRehearsalSession:
    from usa_signal_bot.paper_shadow.rehearsal_runner import PaperShadowRehearsalRunner
    context = shadow_context_from_release_sandbox_review(sandbox_payload)
    runner = PaperShadowRehearsalRunner()
    return runner.run_rehearsal(context)

def attach_shadow_metadata_to_sandbox_review(sandbox_payload: dict[str, Any], session: ShadowRehearsalSession) -> dict[str, Any]:
    sandbox_payload["shadow_rehearsal_id"] = session.session_id
    sandbox_payload["shadow_status"] = session.status.value
    return sandbox_payload

def release_sandbox_shadow_summary(sandbox_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "sandbox_id": sandbox_payload.get("review_id", sandbox_payload.get("sandbox_id")),
        "shadow_rehearsal_id": sandbox_payload.get("shadow_rehearsal_id"),
        "shadow_status": sandbox_payload.get("shadow_status")
    }

def release_sandbox_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = release_sandbox_shadow_summary(payload)
    text = "Release Sandbox Adapter Summary\n"
    for k, v in summary.items():
        text += f"{k}: {v}\n"
    return text
