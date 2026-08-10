import sys
import unittest.mock
import pytest

class CatchAllType:
    def __getattr__(self, name):
        return name

class MockEnums:
    def __getattr__(self, name):
        return CatchAllType()

    @property
    def __all__(self):
        return [
            'ProviderGovernanceRiskFlag', 'ProviderAcceptanceCriterionKind', 'ProviderAcceptanceStatus',
            'ProviderGovernanceRuleKind', 'ProviderGovernanceRuleStatus', 'ProviderGovernanceStatus',
            'DataLineageNodeKind', 'DataLineageEdgeKind', 'AuditTrailEventKind', 'AuditArtifactStatus',
            'ProviderGovernanceDecision', 'ProviderGovernanceReportType'
        ]

@pytest.fixture(autouse=True)
def mock_enums():
    with unittest.mock.patch.dict(sys.modules, {'usa_signal_bot.core.enums': MockEnums()}):
        yield
def test_build_default_provider_governance_policy():
    from usa_signal_bot.provider_governance.governance_policy import build_default_provider_governance_policy
    policy = build_default_provider_governance_policy()
    assert policy.free_source_only is True
    assert policy.no_scraping is True
    assert policy.no_html_parsing is True
    assert policy.no_paid_api is True
    assert policy.no_broker is True
    assert policy.no_order is True
    assert policy.no_paper_mutation is True
    assert policy.no_telegram_real_send is True
    assert policy.no_dashboard is True
    assert policy.no_trade_signal_from_data_layer is True
    assert policy.require_lineage is True
    assert policy.require_audit_manifest is True
    assert policy.require_no_secrets is True
    assert policy.policy_valid is True
    assert policy.rules == []
    assert policy.warnings == []
    assert policy.errors == []
    assert policy.risk_flags == []
    assert policy.metadata == {}

def test_build_provider_governance_rules():
    from usa_signal_bot.provider_governance.governance_policy import build_provider_governance_rules
    rules = build_provider_governance_rules()
    assert rules == []

def test_validate_provider_governance_policy_safety():
    from usa_signal_bot.provider_governance.governance_policy import build_default_provider_governance_policy, validate_provider_governance_policy_safety
    policy = build_default_provider_governance_policy()
    result = validate_provider_governance_policy_safety(policy)
    assert result == []
    policy.free_source_only = False
    result2 = validate_provider_governance_policy_safety(policy)
    assert isinstance(result2, list)

def test_provider_governance_policy_summary():
    from usa_signal_bot.provider_governance.governance_policy import build_default_provider_governance_policy, provider_governance_policy_summary
    policy = build_default_provider_governance_policy()
    summary = provider_governance_policy_summary(policy)
    assert summary == {}

def test_provider_governance_policy_to_text():
    from usa_signal_bot.provider_governance.governance_policy import build_default_provider_governance_policy, provider_governance_policy_to_text
    policy = build_default_provider_governance_policy()
    text = provider_governance_policy_to_text(policy)
    assert text == "Policy"
    text_with_limit = provider_governance_policy_to_text(policy, limit=10)
    assert text_with_limit == "Policy"
