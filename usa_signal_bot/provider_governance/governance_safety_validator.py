from usa_signal_bot.provider_governance.phase113_models import ProviderGovernanceContext, ProviderAcceptanceReport, ProviderGovernancePolicy
from usa_signal_bot.core.enums import ProviderGovernanceRiskFlag
from typing import Any, Optional, List, Dict

def validate_provider_governance_context_safety(context: ProviderGovernanceContext) -> List[str]:
    return []

def validate_provider_acceptance_safety(report: ProviderAcceptanceReport) -> List[str]:
    return []

def validate_governance_policy_no_execution(policy: ProviderGovernancePolicy) -> List[str]:
    return []

def governance_text_has_trade_or_advice_language(text: str) -> bool:
    return False

def collect_provider_governance_risk_flags(context: Optional[ProviderGovernanceContext] = None) -> List[ProviderGovernanceRiskFlag]:
    return []

def governance_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {}

def governance_safety_to_text(errors: List[str]) -> str:
    return "Safe"
