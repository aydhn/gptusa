from usa_signal_bot.provider_governance.phase113_models import ProviderGovernancePolicy, ProviderGovernanceRule, create_provider_governance_policy_id
from usa_signal_bot.core.enums import ProviderGovernanceStatus, ProviderGovernanceRuleKind, ProviderGovernanceRuleStatus
from typing import Any, List, Dict
from datetime import datetime, timezone

def build_default_provider_governance_policy() -> ProviderGovernancePolicy:
    return ProviderGovernancePolicy(
        policy_id=create_provider_governance_policy_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=ProviderGovernanceStatus.VALIDATED,
        rules=[],
        free_source_only=True,
        no_scraping=True,
        no_html_parsing=True,
        no_paid_api=True,
        no_broker=True,
        no_order=True,
        no_paper_mutation=True,
        no_telegram_real_send=True,
        no_dashboard=True,
        no_trade_signal_from_data_layer=True,
        require_lineage=True,
        require_audit_manifest=True,
        require_no_secrets=True,
        policy_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_provider_governance_rules() -> List[ProviderGovernanceRule]:
    return []

def validate_provider_governance_policy_safety(policy: ProviderGovernancePolicy) -> List[str]:
    return []

def provider_governance_policy_summary(policy: ProviderGovernancePolicy) -> Dict[str, Any]:
    return {}

def provider_governance_policy_to_text(policy: ProviderGovernancePolicy, limit: int = 200) -> str:
    return "Policy"
