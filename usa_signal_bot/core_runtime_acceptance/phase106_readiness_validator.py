from typing import Dict, Any, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import DataProviderExpansionKickoffGate

def validate_phase106_data_provider_expansion_readiness(gate: DataProviderExpansionKickoffGate) -> List[str]:
    errors = []
    if not gate.ready_for_phase106:
        errors.append("not ready for phase 106")
    return errors

def phase106_readiness_passed(gate: DataProviderExpansionKickoffGate) -> bool:
    return gate.ready_for_phase106

def phase106_allowed_scope() -> List[str]:
    return [
        "provider adapter abstraction",
        "free data source interface definitions",
        "no-scraping provider contracts",
        "provider selection metadata",
        "provider fallback metadata",
        "provider cache plan",
        "provider data quality plan",
        "provider rate-limit metadata",
        "local test fixtures"
    ]

def phase106_blocked_scope() -> List[str]:
    return [
        "paid API",
        "scraping",
        "HTML parsing",
        "broker execution",
        "order routing",
        "paper state mutation",
        "Telegram real send",
        "dashboard",
        "live/demo trading"
    ]

def phase106_readiness_summary(gate: DataProviderExpansionKickoffGate) -> Dict[str, Any]:
    return {
        "ready": gate.ready_for_phase106
    }

def phase106_readiness_validator_to_text(gate: DataProviderExpansionKickoffGate) -> str:
    return f"Phase 106 Readiness: {'Passed' if phase106_readiness_passed(gate) else 'Failed'}"
