
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderSafetyPolicy, create_provider_safety_policy_id, _now

def build_provider_safety_policy() -> ProviderSafetyPolicy:
    return ProviderSafetyPolicy(
        policy_id=create_provider_safety_policy_id(),
        created_at_utc=_now(),
        metadata_only_by_default=True,
        network_fetch_disabled_now=True,
        paid_api_blocked=True,
        scraping_blocked=True,
        html_parsing_blocked=True,
        broker_blocked=True,
        order_blocked=True,
        paper_mutation_blocked=True,
        telegram_real_send_blocked=True,
        dashboard_blocked=True,
        credential_required_blocked_now=True,
        unknown_license_warning=True,
        unknown_rate_limit_warning=True,
        policy_valid=True
    )

def validate_provider_safety_policy(policy: ProviderSafetyPolicy) -> list[str]:
    return []

def provider_safety_policy_blocks_network_now(policy: ProviderSafetyPolicy) -> bool:
    return policy.network_fetch_disabled_now

def provider_safety_policy_blocks_paid_api(policy: ProviderSafetyPolicy) -> bool:
    return policy.paid_api_blocked

def provider_safety_policy_blocks_scraping(policy: ProviderSafetyPolicy) -> bool:
    return policy.scraping_blocked

def provider_safety_policy_summary(policy: ProviderSafetyPolicy) -> dict[str, Any]:
    return {"valid": policy.policy_valid}

def provider_safety_policy_to_text(policy: ProviderSafetyPolicy) -> str:
    return f"Policy {policy.policy_id}: valid={policy.policy_valid}"
