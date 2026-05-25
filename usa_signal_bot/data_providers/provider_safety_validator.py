
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderAbstractionContext, ProviderSelectionResult, ProviderRegistryEntry
from usa_signal_bot.core.enums import ProviderRiskFlag

def validate_provider_abstraction_safety(context: ProviderAbstractionContext) -> list[str]:
    errs = []
    if not context.metadata_only: errs.append("metadata_only false")
    if context.provider_network_fetch_enabled_now: errs.append("network_fetch_enabled_now true")
    if context.activation_allowed: errs.append("activation_allowed true")
    if context.active_paper_enabled: errs.append("active_paper_enabled true")
    if context.broker_execution_enabled: errs.append("broker_execution_enabled true")
    if context.paper_state_mutation_enabled: errs.append("paper_state_mutation_enabled true")
    if context.telegram_real_send_enabled: errs.append("telegram_real_send_enabled true")
    if context.scraping_enabled: errs.append("scraping_enabled true")
    if context.html_parse_enabled: errs.append("html_parse_enabled true")
    if context.dashboard_enabled: errs.append("dashboard_enabled true")
    if context.paid_api_enabled: errs.append("paid_api_enabled true")
    return errs

def validate_provider_selection_safety(result: ProviderSelectionResult) -> list[str]:
    return []

def collect_provider_risk_flags(context: ProviderAbstractionContext | None = None, entries: list[ProviderRegistryEntry] | None = None) -> list[ProviderRiskFlag]:
    return []

def provider_safety_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"errors": len(errors)}

def provider_safety_validator_to_text(errors: list[str]) -> str:
    return str(errors)
