from typing import Dict, Any, List, Optional
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    LifecycleReviewIngestionResult,
    CoreRuntimeAcceptanceReport,
    AdvancedFoundationFreezeBundle,
    DataProviderExpansionKickoffGate,
    CoreRuntimeAcceptanceRiskFlag
)

def validate_phase105_no_execution_safety(
    lifecycle: Optional[LifecycleReviewIngestionResult] = None,
    acceptance_report: Optional[CoreRuntimeAcceptanceReport] = None,
    freeze: Optional[AdvancedFoundationFreezeBundle] = None,
    gate: Optional[DataProviderExpansionKickoffGate] = None
) -> List[str]:
    errors = []
    objects = [lifecycle, acceptance_report, freeze, gate]
    for obj in objects:
        if not obj: continue
        if getattr(obj, "activation_allowed", False): errors.append("activation_allowed")
        if getattr(obj, "active_paper_enabled", False): errors.append("active_paper_enabled")
        if getattr(obj, "broker_execution_enabled", False): errors.append("broker_execution_enabled")
        if getattr(obj, "paper_state_mutation_enabled", False): errors.append("paper_state_mutation_enabled")
        if getattr(obj, "telegram_real_send_enabled", False): errors.append("telegram_real_send_enabled")
        if getattr(obj, "scraping_enabled", False): errors.append("scraping_enabled")
        if getattr(obj, "html_parse_enabled", False): errors.append("html_parse_enabled")
        if getattr(obj, "dashboard_enabled", False): errors.append("dashboard_enabled")
        if getattr(obj, "paid_api_enabled", False): errors.append("paid_api_enabled")
        if getattr(obj, "provider_network_fetch_required", False): errors.append("provider_network_fetch_required")
        if getattr(obj, "execution_performed", False): errors.append("execution_performed")
        if getattr(obj, "network_used", False): errors.append("network_used")
        if getattr(obj, "broker_used", False): errors.append("broker_used")
        if getattr(obj, "order_created", False): errors.append("order_created")
        if getattr(obj, "paper_state_mutated", False): errors.append("paper_state_mutated")
        if getattr(obj, "telegram_real_sent", False): errors.append("telegram_real_sent")
        if getattr(obj, "scraping_used", False): errors.append("scraping_used")
        if getattr(obj, "dashboard_started", False): errors.append("dashboard_started")
    return list(set(errors))

def collect_phase105_no_execution_risk_flags(
    lifecycle: Optional[LifecycleReviewIngestionResult] = None,
    acceptance_report: Optional[CoreRuntimeAcceptanceReport] = None,
    freeze: Optional[AdvancedFoundationFreezeBundle] = None,
    gate: Optional[DataProviderExpansionKickoffGate] = None
) -> List[CoreRuntimeAcceptanceRiskFlag]:
    return []

def phase105_no_execution_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safe": len(errors) == 0, "errors": errors}

def phase105_no_execution_safety_to_text(errors: List[str]) -> str:
    return f"No-Execution Safety: {'Passed' if len(errors) == 0 else 'Failed'}"
