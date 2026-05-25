
from typing import Any, Dict, List

def build_default_event_impact_policy() -> Dict[str, Any]:
    return {
        "metadata_only": True,
        "research_context_only": True,
        "produce_trade_signals": False,
        "produce_order_decisions": False,
        "allow_network": False,
        "allow_paid_api": False,
        "allow_scraping": False,
        "allow_html_parsing": False,
        "allow_broker": False,
        "allow_order": False,
        "allow_paper_mutation": False,
        "allow_telegram_real_send": False,
        "allow_dashboard": False
    }

def validate_event_impact_policy(policy: Dict[str, Any]) -> List[str]:
    errors = []
    if not policy.get("metadata_only", False): errors.append("metadata_only must be true")
    if not policy.get("research_context_only", False): errors.append("research_context_only must be true")

    for key in ["produce_trade_signals", "produce_order_decisions", "allow_network", "allow_paid_api",
                "allow_scraping", "allow_html_parsing", "allow_broker", "allow_order",
                "allow_paper_mutation", "allow_telegram_real_send", "allow_dashboard"]:
        if policy.get(key, True):
            errors.append(f"{key} must be false")

    return errors

def impact_policy_allows_trade_signal(policy: Dict[str, Any]) -> bool:
    return policy.get("produce_trade_signals", False)

def impact_policy_allows_order_decision(policy: Dict[str, Any]) -> bool:
    return policy.get("produce_order_decisions", False)

def impact_policy_to_text(policy: Dict[str, Any]) -> str:
    return f"Event Impact Policy: valid={len(validate_event_impact_policy(policy)) == 0}"
