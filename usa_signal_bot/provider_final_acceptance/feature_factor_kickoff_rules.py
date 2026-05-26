from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    FeatureFactorKickoffRule,
    FeatureFactorKickoffRuleStatus,
    DataProviderFinalAcceptanceReport,
    ProviderLayerClosureBundle,
    FeatureFactorDataContract,
    create_feature_factor_kickoff_rule_id,
    _utc_now
)

def required_feature_factor_kickoff_rule_names() -> list[str]:
    return [
        "data_provider_layer_accepted",
        "provider_layer_closed",
        "final_data_contract_valid",
        "no_trade_signal_allowed",
        "no_order_decision_allowed",
        "no_broker_allowed",
        "no_scraping_allowed",
        "no_paid_api_allowed"
    ]

def rule_data_provider_layer_accepted(acceptance: DataProviderFinalAcceptanceReport) -> FeatureFactorKickoffRule:
    passed = acceptance.data_provider_layer_accepted
    return FeatureFactorKickoffRule(
        rule_id=create_feature_factor_kickoff_rule_id(),
        created_at_utc=_utc_now(),
        rule_name="data_provider_layer_accepted",
        status=FeatureFactorKickoffRuleStatus.PASS if passed else FeatureFactorKickoffRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description="Data provider layer must be accepted.",
        risk_flags=[],
        warnings=[],
        errors=[] if passed else ["Data provider layer not accepted."],
        metadata={}
    )

def rule_provider_layer_closed(closure: ProviderLayerClosureBundle) -> FeatureFactorKickoffRule:
    passed = closure.closed
    return FeatureFactorKickoffRule(
        rule_id=create_feature_factor_kickoff_rule_id(),
        created_at_utc=_utc_now(),
        rule_name="provider_layer_closed",
        status=FeatureFactorKickoffRuleStatus.PASS if passed else FeatureFactorKickoffRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description="Provider layer must be closed.",
        risk_flags=[],
        warnings=[],
        errors=[] if passed else ["Provider layer not closed."],
        metadata={}
    )

def rule_final_data_contract_valid(contract: FeatureFactorDataContract) -> FeatureFactorKickoffRule:
    passed = contract.contract_valid
    return FeatureFactorKickoffRule(
        rule_id=create_feature_factor_kickoff_rule_id(),
        created_at_utc=_utc_now(),
        rule_name="final_data_contract_valid",
        status=FeatureFactorKickoffRuleStatus.PASS if passed else FeatureFactorKickoffRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description="Final data contract must be valid.",
        risk_flags=[],
        warnings=[],
        errors=[] if passed else ["Final data contract not valid."],
        metadata={}
    )

def rule_no_trade_signal_allowed(contract: FeatureFactorDataContract) -> FeatureFactorKickoffRule:
    passed = contract.trade_signal_blocked
    return FeatureFactorKickoffRule(
        rule_id=create_feature_factor_kickoff_rule_id(),
        created_at_utc=_utc_now(),
        rule_name="no_trade_signal_allowed",
        status=FeatureFactorKickoffRuleStatus.PASS if passed else FeatureFactorKickoffRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description="Trade signal generation must be blocked.",
        risk_flags=[],
        warnings=[],
        errors=[] if passed else ["Trade signal allowed."],
        metadata={}
    )

def rule_no_order_decision_allowed(contract: FeatureFactorDataContract) -> FeatureFactorKickoffRule:
    passed = contract.order_decision_blocked
    return FeatureFactorKickoffRule(
        rule_id=create_feature_factor_kickoff_rule_id(),
        created_at_utc=_utc_now(),
        rule_name="no_order_decision_allowed",
        status=FeatureFactorKickoffRuleStatus.PASS if passed else FeatureFactorKickoffRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description="Order decision must be blocked.",
        risk_flags=[],
        warnings=[],
        errors=[] if passed else ["Order decision allowed."],
        metadata={}
    )

def rule_no_broker_allowed(contract: FeatureFactorDataContract) -> FeatureFactorKickoffRule:
    passed = contract.broker_blocked
    return FeatureFactorKickoffRule(
        rule_id=create_feature_factor_kickoff_rule_id(),
        created_at_utc=_utc_now(),
        rule_name="no_broker_allowed",
        status=FeatureFactorKickoffRuleStatus.PASS if passed else FeatureFactorKickoffRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description="Broker execution must be blocked.",
        risk_flags=[],
        warnings=[],
        errors=[] if passed else ["Broker execution allowed."],
        metadata={}
    )

def rule_no_scraping_allowed(contract: FeatureFactorDataContract) -> FeatureFactorKickoffRule:
    passed = contract.scraping_blocked
    return FeatureFactorKickoffRule(
        rule_id=create_feature_factor_kickoff_rule_id(),
        created_at_utc=_utc_now(),
        rule_name="no_scraping_allowed",
        status=FeatureFactorKickoffRuleStatus.PASS if passed else FeatureFactorKickoffRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description="Scraping must be blocked.",
        risk_flags=[],
        warnings=[],
        errors=[] if passed else ["Scraping allowed."],
        metadata={}
    )

def rule_no_paid_api_allowed(contract: FeatureFactorDataContract) -> FeatureFactorKickoffRule:
    passed = contract.paid_api_blocked
    return FeatureFactorKickoffRule(
        rule_id=create_feature_factor_kickoff_rule_id(),
        created_at_utc=_utc_now(),
        rule_name="no_paid_api_allowed",
        status=FeatureFactorKickoffRuleStatus.PASS if passed else FeatureFactorKickoffRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description="Paid APIs must be blocked.",
        risk_flags=[],
        warnings=[],
        errors=[] if passed else ["Paid API allowed."],
        metadata={}
    )

def build_feature_factor_kickoff_rules(acceptance: DataProviderFinalAcceptanceReport, closure: ProviderLayerClosureBundle, contract: FeatureFactorDataContract) -> list[FeatureFactorKickoffRule]:
    return [
        rule_data_provider_layer_accepted(acceptance),
        rule_provider_layer_closed(closure),
        rule_final_data_contract_valid(contract),
        rule_no_trade_signal_allowed(contract),
        rule_no_order_decision_allowed(contract),
        rule_no_broker_allowed(contract),
        rule_no_scraping_allowed(contract),
        rule_no_paid_api_allowed(contract)
    ]

def feature_factor_kickoff_rules_summary(rules: list[FeatureFactorKickoffRule]) -> dict[str, Any]:
    return {
        "total": len(rules),
        "passed": sum(1 for r in rules if r.status == FeatureFactorKickoffRuleStatus.PASS),
        "failed": sum(1 for r in rules if r.status == FeatureFactorKickoffRuleStatus.FAIL)
    }

def feature_factor_kickoff_rules_to_text(rules: list[FeatureFactorKickoffRule], limit: int = 200) -> str:
    s = feature_factor_kickoff_rules_summary(rules)
    return f"Rules: {s['passed']}/{s['total']} passed."
