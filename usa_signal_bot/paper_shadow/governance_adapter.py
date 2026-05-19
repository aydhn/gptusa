from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def governance_shadow_allowed(governance_payload: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings = []
    if governance_payload.get("decision") != "APPROVE":
        warnings.append("Governance decision is not APPROVE")
    return True, warnings # Shadow is generally allowed even if governance fails

def shadow_rehearsal_governance_checklist(session: ShadowRehearsalSession) -> list[dict[str, Any]]:
    return [
        {"check": "No Real Orders", "passed": not any(i.is_real_order for i in session.order_intents)},
        {"check": "No Paper Mutation", "passed": not (session.context and session.context.allow_paper_state_mutation)},
        {"check": "No Real Telegram Send", "passed": not (session.context and session.context.allow_telegram_real_send)}
    ]

def attach_shadow_rehearsal_to_governance_payload(governance_payload: dict[str, Any], session: ShadowRehearsalSession) -> dict[str, Any]:
    governance_payload["shadow_rehearsal_id"] = session.session_id
    governance_payload["shadow_checklist"] = shadow_rehearsal_governance_checklist(session)
    return governance_payload

def governance_shadow_summary(governance_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "governance_id": governance_payload.get("governance_id", governance_payload.get("id")),
        "shadow_rehearsal_id": governance_payload.get("shadow_rehearsal_id"),
        "shadow_checklist_pass": all(c.get("passed", False) for c in governance_payload.get("shadow_checklist", []))
    }

def governance_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = governance_shadow_summary(payload)
    text = "Governance Shadow Adapter Summary\n"
    for k, v in summary.items():
         text += f"{k}: {v}\n"
    return text
