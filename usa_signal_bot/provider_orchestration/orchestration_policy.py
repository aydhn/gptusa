from typing import Any

def build_default_provider_orchestration_policy() -> dict[str, Any]:
    return {
        "metadata_only": True,
        "research_data_only": True,
        "cache_only_default": True,
        "allow_blending": True,
        "allow_fallback": True,
        "allow_network": False,
        "allow_paid_api": False,
        "allow_scraping": False,
        "allow_html_parsing": False,
        "allow_broker": False,
        "allow_order": False,
        "allow_paper_mutation": False,
        "allow_telegram_real_send": False,
        "allow_dashboard": False,
        "produce_trade_signals": False,
        "produce_order_decisions": False,
    }

def validate_provider_orchestration_policy(policy: dict[str, Any]) -> list[str]:
    errors = []
    if not policy.get("metadata_only", False):
        errors.append("metadata_only must be True")
    if not policy.get("research_data_only", False):
        errors.append("research_data_only must be True")
    if not policy.get("cache_only_default", False):
        errors.append("cache_only_default must be True")

    # Must all be false
    for flag in ["allow_network", "allow_paid_api", "allow_scraping", "allow_html_parsing",
                 "allow_broker", "allow_order", "allow_paper_mutation", "allow_telegram_real_send",
                 "allow_dashboard", "produce_trade_signals", "produce_order_decisions"]:
        if policy.get(flag, True):
            errors.append(f"{flag} must be False")

    return errors

def orchestration_policy_allows_blending(policy: dict[str, Any]) -> bool:
    return policy.get("allow_blending", True)

def orchestration_policy_allows_refresh_planning(policy: dict[str, Any]) -> bool:
    return True

def orchestration_policy_to_text(policy: dict[str, Any]) -> str:
    lines = ["--- Orchestration Policy ---"]
    for k, v in policy.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)
