import pytest
from datetime import datetime

from usa_signal_bot.provider_governance.governance_policy import (
    build_default_provider_governance_policy,
    build_provider_governance_rules,
    validate_provider_governance_policy_safety,
    provider_governance_policy_summary,
    provider_governance_policy_to_text
)
from usa_signal_bot.provider_governance.phase113_models import ProviderGovernancePolicy

def test_build_default_provider_governance_policy():
    policy = build_default_provider_governance_policy()
    assert isinstance(policy, ProviderGovernancePolicy)
    assert policy.policy_id is not None
    assert hasattr(policy, 'status')
    assert policy.free_source_only is True

def test_build_provider_governance_rules():
    rules = build_provider_governance_rules()
    assert isinstance(rules, list)
    assert len(rules) == 0

def test_validate_provider_governance_policy_safety():
    policy = build_default_provider_governance_policy()
    errors = validate_provider_governance_policy_safety(policy)
    assert isinstance(errors, list)
    assert len(errors) == 0

def test_provider_governance_policy_summary():
    policy = build_default_provider_governance_policy()
    summary = provider_governance_policy_summary(policy)
    assert isinstance(summary, dict)
    assert len(summary) == 0

def test_provider_governance_policy_to_text():
    policy = build_default_provider_governance_policy()
    text = provider_governance_policy_to_text(policy)
    assert isinstance(text, str)
    assert text == "Policy"
