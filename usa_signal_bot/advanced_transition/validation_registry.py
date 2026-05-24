from typing import Dict, List

def required_validation_domains() -> List[str]:
    return [
        "no_broker_execution", "no_live_order", "no_demo_order", "no_paper_order",
        "no_paper_state_mutation", "no_telegram_real_send", "no_scraping",
        "no_dashboard", "no_paid_api", "no_investment_advice_language",
        "config_safety", "storage_safety", "import_safety", "runtime_boundary_safety"
    ]

def build_validation_registry() -> Dict[str, List[str]]:
    return {domain: ["Valid"] for domain in required_validation_domains()}

def validate_validation_registry(registry: Dict[str, List[str]]) -> List[str]:
    errors = []
    for d in required_validation_domains():
        if d not in registry:
            errors.append(f"Missing domain: {d}")
    return errors

def validation_registry_to_text(registry: Dict[str, List[str]]) -> str:
    return "\n".join([f"{k}: {len(v)} rules" for k, v in registry.items()])
