from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.core.enums import ShadowFillStatus, ShadowOrderIntentStatus

def analyze_shadow_rehearsal_session(session: ShadowRehearsalSession) -> dict[str, Any]:
    return {
        "metrics": shadow_rehearsal_metrics(session),
        "success_flags": shadow_rehearsal_success_flags(session),
        "warning_flags": shadow_rehearsal_warning_flags(session),
        "block_flags": shadow_rehearsal_block_flags(session)
    }

def shadow_rehearsal_success_flags(session: ShadowRehearsalSession) -> list[str]:
    flags = []
    if session.status.name == "COMPLETED":
        flags.append("SESSION_COMPLETED")
    if not shadow_rehearsal_block_flags(session):
         flags.append("NO_BLOCKS")
    return flags

def shadow_rehearsal_warning_flags(session: ShadowRehearsalSession) -> list[str]:
    return session.warnings.copy()

def shadow_rehearsal_block_flags(session: ShadowRehearsalSession) -> list[str]:
    return session.errors.copy()

def shadow_rehearsal_metrics(session: ShadowRehearsalSession) -> dict[str, Any]:
    approved_intents = sum(1 for i in session.order_intents if i.status == ShadowOrderIntentStatus.RISK_APPROVED)
    blocked_intents = sum(1 for i in session.order_intents if i.status == ShadowOrderIntentStatus.BLOCKED)
    sim_fills = sum(1 for f in session.fills if f.status == ShadowFillStatus.SIMULATED_FILLED)
    pnl = session.pnl_snapshots[-1].total_pnl_usd if session.pnl_snapshots else 0.0

    return {
        "signal_count": len(session.signals),
        "intent_count": len(session.order_intents),
        "approved_intent_count": approved_intents,
        "blocked_intent_count": blocked_intents,
        "simulated_fill_count": sim_fills,
        "shadow_trade_count": sim_fills,
        "simulated_total_cost_usd": sum(f.simulated_cost_usd for f in session.fills),
        "simulated_pnl_usd": pnl,
        "safety_flag_count": len(session.safety_flags)
    }

def shadow_result_analyzer_to_text(payload: dict[str, Any]) -> str:
    text = "Shadow Result Analysis\n"
    for k, v in payload.get("metrics", {}).items():
        text += f"{k}: {v}\n"
    if payload.get("block_flags"):
        text += "Blocks: " + ", ".join(payload["block_flags"]) + "\n"
    if payload.get("warning_flags"):
        text += "Warnings: " + ", ".join(payload["warning_flags"]) + "\n"
    return text
