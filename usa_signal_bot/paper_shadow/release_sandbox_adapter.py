from typing import Any, Dict
from usa_signal_bot.paper_shadow.shadow_models import ShadowSimulationContext, ShadowRehearsalSession
from usa_signal_bot.paper_shadow.simulation_context import build_shadow_simulation_context_from_sandbox_payload
from usa_signal_bot.paper_shadow.rehearsal_runner import PaperShadowRehearsalRunner

def shadow_context_from_release_sandbox_review(sandbox_payload: Dict[str, Any]) -> ShadowSimulationContext:
    return build_shadow_simulation_context_from_sandbox_payload(sandbox_payload)

def shadow_rehearsal_from_sandbox_review(sandbox_payload: Dict[str, Any]) -> ShadowRehearsalSession:
    context = shadow_context_from_release_sandbox_review(sandbox_payload)
    runner = PaperShadowRehearsalRunner()
    return runner.run_rehearsal(context)

def attach_shadow_metadata_to_sandbox_review(sandbox_payload: Dict[str, Any], session: ShadowRehearsalSession) -> Dict[str, Any]:
    sandbox_payload["shadow_rehearsal_metadata"] = {
        "session_id": session.session_id,
        "status": session.status.value,
        "safety_safe": len(session.safety_flags) == 0
    }
    return sandbox_payload

def release_sandbox_shadow_summary(sandbox_payload: Dict[str, Any]) -> Dict[str, Any]:
    return sandbox_payload.get("shadow_rehearsal_metadata", {})

def release_sandbox_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"SandboxShadowMetadata({payload})"
