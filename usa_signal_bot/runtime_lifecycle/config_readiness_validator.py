from typing import List, Dict, Any, Optional

def validate_config_readiness(config: Optional[Dict[str, Any]] = None) -> List[str]:
    errors = []
    if config:
        if config.get("allow_activation", False):
            errors.append("Config allows activation")
        if config.get("allow_active_paper", False):
            errors.append("Config allows active paper")
        if config.get("allow_broker_execution", False):
            errors.append("Config allows broker execution")
        if config.get("allow_paper_state_mutation", False):
            errors.append("Config allows paper state mutation")
        if config.get("allow_telegram_real_send", False):
            errors.append("Config allows Telegram real send")
        if config.get("allow_scraping", False):
            errors.append("Config allows scraping")
        if config.get("allow_dashboard", False):
            errors.append("Config allows dashboard")
        if config.get("allow_paid_api", False):
            errors.append("Config allows paid API")
    return errors

def config_readiness_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors": errors}

def config_readiness_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Config is ready."
    return "Config errors:\n" + "\n".join([f"- {e}" for e in errors])
