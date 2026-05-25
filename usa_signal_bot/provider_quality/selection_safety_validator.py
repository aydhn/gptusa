from typing import List, Dict, Any, Optional
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderSelectionScore,
    ProviderRanking,
    ProviderQualityContext
)
from usa_signal_bot.core.enums import ProviderQualityRiskFlag

def validate_provider_selection_safety(score: ProviderSelectionScore) -> List[str]:
    errors = []
    if score.decision.value in ["PREFER_FOR_RESEARCH_DATA", "USE_AS_FALLBACK_DATA", "USE_WITH_DATA_WARNING"]:
        if "trade signal" in score.explanation.lower() or "order" in score.explanation.lower():
            errors.append("Explanation contains unsafe execution language")

    # We implicitly trust the dataclass fields since they are validated upon instantiation,
    # but we double check logical safety invariants here.
    if not score.selectable_for_research and score.decision.value == "PREFER_FOR_RESEARCH_DATA":
        errors.append("Score decision contradicts research selection capability")

    return errors

def validate_provider_ranking_safety(ranking: ProviderRanking) -> List[str]:
    errors = []
    if not ranking.ranking_is_research_data_only:
        errors.append("ranking_is_research_data_only must be True")
    if ranking.produces_trade_signal:
        errors.append("produces_trade_signal must be False")
    if ranking.produces_order_decision:
        errors.append("produces_order_decision must be False")
    return errors

def validate_provider_quality_context_safety(context: ProviderQualityContext) -> List[str]:
    errors = []
    if not context.research_data_only: errors.append("research_data_only is False")
    if context.produces_trade_signal: errors.append("produces_trade_signal is True")
    if context.produces_order_decision: errors.append("produces_order_decision is True")
    if context.network_used: errors.append("network_used is True")
    if context.paid_api_used: errors.append("paid_api_used is True")
    if context.scraping_used: errors.append("scraping_used is True")
    if context.html_parsing_used: errors.append("html_parsing_used is True")
    if context.broker_used: errors.append("broker_used is True")
    if context.order_created: errors.append("order_created is True")
    if context.paper_state_mutated: errors.append("paper_state_mutated is True")
    if context.telegram_real_sent: errors.append("telegram_real_sent is True")
    if context.dashboard_started: errors.append("dashboard_started is True")
    return errors

def collect_provider_quality_risk_flags(context: Optional[ProviderQualityContext] = None) -> List[ProviderQualityRiskFlag]:
    flags = []
    if not context:
        return flags
    flags.extend(context.risk_flags)
    for q in context.data_quality_scores:
        flags.extend(q.risk_flags)
        for c in q.components:
            flags.extend(c.risk_flags)
    for t in context.trust_profiles:
        flags.extend(t.risk_flags)
    for s in context.selection_scores:
        flags.extend(s.risk_flags)
    for r in context.rankings:
        flags.extend(r.risk_flags)

    return list(set(flags))

def selection_safety_validator_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "safe": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def selection_safety_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Selection Safety Validator: PASSED"
    return "Selection Safety Validator: FAILED\n  " + "\n  ".join(errors)
