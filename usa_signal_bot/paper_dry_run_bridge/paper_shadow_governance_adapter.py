from typing import Any, Tuple, List
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunBridgeSession

def dry_run_candidate_refs_from_shadow_governance(payload: dict[str, Any]) -> dict[str, Any]:
    candidate_id = payload.get("candidate_id") or payload.get("id")
    return {
        "candidate_id": candidate_id,
        "shadow_review_id": payload.get("review_id")
    }

def shadow_governance_supports_dry_run(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    # In a real impl, we'd check if shadow governance actually passed
    return True, warnings

def attach_dry_run_hint_to_shadow_governance(payload: dict[str, Any], session: DryRunBridgeSession) -> dict[str, Any]:
    result = payload.copy()
    result["dry_run_hint"] = {
        "session_id": session.session_id,
        "status": session.status.value
    }
    return result

def paper_shadow_governance_dry_run_summary(payload: dict[str, Any]) -> dict[str, Any]:
    hint = payload.get("dry_run_hint", {})
    return {
        "has_dry_run_hint": bool(hint),
        "session_id": hint.get("session_id")
    }

def paper_shadow_governance_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = paper_shadow_governance_dry_run_summary(payload)
    return f"Shadow Governance Adapter: Hint Attached={summary['has_dry_run_hint']}"
