import pytest

from usa_signal_bot.provider_governance.governance_policy import (
    build_default_provider_governance_policy,
    build_provider_governance_rules,
    validate_provider_governance_policy_safety,
    provider_governance_policy_summary,
    provider_governance_policy_to_text,
)

def test_build_default_provider_governance_policy():
    policy = build_default_provider_governance_policy()
    assert policy.policy_id is not None
    assert policy.free_source_only is True
    assert policy.no_scraping is True

def test_build_provider_governance_rules():
    rules = build_provider_governance_rules()
    assert isinstance(rules, list)
    assert len(rules) == 0

def test_validate_provider_governance_policy_safety():
    policy = build_default_provider_governance_policy()
    issues = validate_provider_governance_policy_safety(policy)
    assert isinstance(issues, list)
    assert len(issues) == 0

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

    # Test with custom limit
    text_with_limit = provider_governance_policy_to_text(policy, limit=10)
    assert isinstance(text_with_limit, str)
    assert text_with_limit == "Policy"
