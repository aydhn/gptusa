from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
from usa_signal_bot.core.enums import ShadowSessionStatus

def analyze_shadow_rehearsal_session(session: ShadowRehearsalSession) -> Dict[str, Any]:
    return {
        "metrics": shadow_rehearsal_metrics(session),
        "success_flags": shadow_rehearsal_success_flags(session),
        "warning_flags": shadow_rehearsal_warning_flags(session),
        "block_flags": shadow_rehearsal_block_flags(session)
    }

def shadow_rehearsal_success_flags(session: ShadowRehearsalSession) -> List[str]:
    flags = []
    if session.status == ShadowSessionStatus.COMPLETED:
        flags.append("SESSION_COMPLETED")
    if len(session.fills) > 0 and any(f.status == "SIMULATED_FILLED" for f in session.fills):
        flags.append("HAS_SIMULATED_FILLS")
    return flags

def shadow_rehearsal_warning_flags(session: ShadowRehearsalSession) -> List[str]:
    flags = []
    if session.warnings:
        flags.append("SESSION_WARNINGS")
    if any(i.status == "RISK_REJECTED" for i in session.order_intents):
        flags.append("INTENTS_REJECTED_BY_RISK")
    return flags

def shadow_rehearsal_block_flags(session: ShadowRehearsalSession) -> List[str]:
    flags = []
    if session.status == ShadowSessionStatus.FAILED:
        flags.append("SESSION_FAILED")
    if session.errors:
        flags.append("SESSION_ERRORS")
    if session.safety_flags:
        flags.append("SAFETY_FLAGS_TRIGGERED")
    return flags

def shadow_rehearsal_metrics(session: ShadowRehearsalSession) -> Dict[str, Any]:
    pnl = 0.0
    if session.pnl_snapshots:
        pnl = session.pnl_snapshots[-1].total_pnl_usd

    return {
        "signal_count": len(session.signals),
        "candidate_count": len([s for s in session.signals if s.score and s.score >= 50.0]), # Approx
        "intent_count": len(session.order_intents),
        "approved_intent_count": sum(1 for i in session.order_intents if i.status == "RISK_APPROVED"),
        "blocked_intent_count": sum(1 for i in session.order_intents if i.status == "BLOCKED"),
        "simulated_fill_count": sum(1 for f in session.fills if f.status == "SIMULATED_FILLED"),
        "shadow_trade_count": len(session.fills),
        "simulated_total_cost_usd": sum(f.simulated_cost_usd + f.simulated_slippage_usd for f in session.fills),
        "simulated_pnl_usd": pnl,
        "safety_flag_count": len(session.safety_flags)
    }

def shadow_result_analyzer_to_text(payload: Dict[str, Any]) -> str:
    m = payload.get("metrics", {})
    return f"AnalyzerResult(fills={m.get('simulated_fill_count', 0)}, pnl={m.get('simulated_pnl_usd', 0.0):.2f})"
