from typing import Dict, Any, List

def collect_config_sections(config: Dict[str, Any]) -> Dict[str, Any]:
    return config

def build_phase101_config_consolidation_report(config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "CONSOLIDATED",
        "errors": validate_core_config_sections(config) + validate_no_execution_config_enabled(config)
    }

def validate_core_config_sections(config: Dict[str, Any]) -> List[str]:
    errors = []
    return errors

def validate_no_execution_config_enabled(config: Dict[str, Any]) -> List[str]:
    errors = []
    at_cfg = config.get("advanced_transition", {})
    if at_cfg.get("allow_broker_execution", False): errors.append("allow_broker_execution must be False")
    if at_cfg.get("allow_active_paper", False): errors.append("allow_active_paper must be False")
    if at_cfg.get("allow_paper_state_mutation", False): errors.append("allow_paper_state_mutation must be False")
    if at_cfg.get("allow_telegram_real_send", False): errors.append("allow_telegram_real_send must be False")
    if at_cfg.get("allow_scraping", False): errors.append("allow_scraping must be False")
    if at_cfg.get("allow_dashboard", False): errors.append("allow_dashboard must be False")
    return errors

def config_consolidation_to_text(report: Dict[str, Any]) -> str:
    return f"Config Consolidation Status: {report.get('status')}\nErrors: {report.get('errors')}"
