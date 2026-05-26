from typing import Any, Dict

def build_default_provider_freeze_policy() -> Dict[str, Any]:
    return {
        "metadata_only": True,
        "research_data_only": True,
        "phase_start": 106,
        "phase_end": 114,
        "next_phase": 115,
        "final_phase": 160,
        "frozen": True,
        "immutable": True,
        "allow_activation": False,
        "allow_active_paper": False,
        "allow_broker_execution": False,
        "allow_order_creation": False,
        "allow_paper_mutation": False,
        "allow_telegram_real_send": False,
        "allow_scraping": False,
        "allow_html_parsing": False,
        "allow_paid_api": False,
        "allow_dashboard": False,
        "network_default_enabled": False,
        "produce_trade_signals": False,
        "produce_order_decisions": False
    }

def validate_provider_freeze_policy(policy: Dict[str, Any]) -> list[str]:
    errors = []
    if not policy.get("metadata_only"):
        errors.append("metadata_only must be True")
    if not policy.get("research_data_only"):
        errors.append("research_data_only must be True")
    if policy.get("phase_start") != 106:
        errors.append("phase_start must be 106")
    if policy.get("phase_end") != 114:
        errors.append("phase_end must be 114")
    if policy.get("next_phase") != 115:
        errors.append("next_phase must be 115")
    if policy.get("final_phase") != 160:
        errors.append("final_phase must be 160")
    if not policy.get("frozen"):
        errors.append("frozen must be True")
    if not policy.get("immutable"):
        errors.append("immutable must be True")

    for k in [
        "allow_activation", "allow_active_paper", "allow_broker_execution",
        "allow_order_creation", "allow_paper_mutation", "allow_telegram_real_send",
        "allow_scraping", "allow_html_parsing", "allow_paid_api", "allow_dashboard",
        "network_default_enabled", "produce_trade_signals", "produce_order_decisions"
    ]:
        if policy.get(k):
            errors.append(f"{k} must be False")

    return errors

def provider_freeze_policy_allows_activation(policy: Dict[str, Any]) -> bool:
    return policy.get("allow_activation", False)

def provider_freeze_policy_allows_network_default(policy: Dict[str, Any]) -> bool:
    return policy.get("network_default_enabled", False)

def provider_freeze_policy_to_text(policy: Dict[str, Any]) -> str:
    lines = ["Provider Freeze Policy:"]
    for k, v in policy.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)
