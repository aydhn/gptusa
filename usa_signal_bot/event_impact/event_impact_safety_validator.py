
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import EventImpactRiskFlag
from usa_signal_bot.event_impact.phase112_models import EventImpactContext, EventImpactTag, MacroRegimeMetadata

def event_impact_text_has_trade_language(text: str) -> bool:
    t = text.lower()
    unsafe = [
        "buy", "sell", "strong buy", "strong sell", "emir gönderildi",
        "aktif trading", "paper'a alındı", "canlıya alındı", "kesin al",
        "kesin sat", "garanti kâr", "trade signal", "order routing"
    ]
    return any(u in t for u in unsafe)

def validate_impact_tags_safety(tags: List[EventImpactTag]) -> List[str]:
    errs = []
    for tag in tags:
        if tag.produces_trade_signal or tag.produces_order_decision:
            errs.append(f"Tag {tag.impact_tag_id} produces signals")
        if event_impact_text_has_trade_language(tag.explanation):
            errs.append(f"Tag {tag.impact_tag_id} contains trade language")
    return errs

def validate_macro_regime_safety(items: List[MacroRegimeMetadata]) -> List[str]:
    errs = []
    for m in items:
        if m.produces_trade_signal or m.produces_order_decision:
            errs.append(f"Regime {m.regime_id} produces signals")
        if event_impact_text_has_trade_language(m.description):
            errs.append(f"Regime {m.regime_id} contains trade language")
    return errs

def validate_event_impact_context_safety(context: EventImpactContext) -> List[str]:
    errs = []
    if context.produces_trade_signal or context.produces_order_decision:
        errs.append("Context produces trade signals or order decisions.")
    if context.network_used or context.paid_api_used or context.scraping_used or context.html_parsing_used:
        errs.append("Context used forbidden network/scraping tools.")
    if context.broker_used or context.order_created or context.paper_state_mutated or context.telegram_real_sent or context.dashboard_started:
        errs.append("Context used execution or dashboard tools.")

    errs.extend(validate_impact_tags_safety(context.impact_tags))
    errs.extend(validate_macro_regime_safety(context.macro_regimes))
    return errs

def collect_event_impact_risk_flags(context: Optional[EventImpactContext] = None) -> List[EventImpactRiskFlag]:
    flags = set()
    if not context:
        return []

    if context.produces_trade_signal: flags.add(EventImpactRiskFlag.IMPACT_TAG_TRADE_SIGNAL_RISK)
    if context.network_used: flags.add(EventImpactRiskFlag.NETWORK_FETCH_ATTEMPTED)
    if context.broker_used: flags.add(EventImpactRiskFlag.BROKER_RISK)
    if context.telegram_real_sent: flags.add(EventImpactRiskFlag.TELEGRAM_REAL_SEND_RISK)
    if context.paper_state_mutated: flags.add(EventImpactRiskFlag.PAPER_MUTATION_RISK)

    return list(flags)

def event_impact_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors), "safe": len(errors) == 0}

def event_impact_safety_to_text(errors: List[str]) -> str:
    if not errors: return "All safe."
    return "SAFETY VIOLATIONS:\n" + "\n".join(errors)
