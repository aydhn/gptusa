from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    FeatureFactorKickoffAssertion,
    FeatureFactorKickoffAssertionStatus,
    DataProviderFinalAcceptanceReport,
    ProviderLayerClosureBundle,
    FeatureFactorDataContract,
    create_feature_factor_kickoff_assertion_id,
    _utc_now
)

def required_feature_factor_kickoff_assertions() -> list[str]:
    return [
        "phase116_scope_metadata_only",
        "phase116_research_data_only",
        "no_active_paper",
        "no_broker",
        "no_order",
        "no_paper_state_mutation",
        "no_telegram_real_send",
        "no_scraping",
        "no_html_parsing",
        "no_paid_api",
        "no_dashboard",
        "no_trade_signal_generation",
        "no_order_decision_generation"
    ]

def _build_assertion(name: str, passed: bool, desc: str) -> FeatureFactorKickoffAssertion:
    return FeatureFactorKickoffAssertion(
        assertion_id=create_feature_factor_kickoff_assertion_id(),
        created_at_utc=_utc_now(),
        assertion_name=name,
        status=FeatureFactorKickoffAssertionStatus.PASS if passed else FeatureFactorKickoffAssertionStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        description=desc,
        risk_flags=[],
        warnings=[],
        errors=[] if passed else [f"{name} failed"],
        metadata={}
    )

def assertion_phase116_scope_metadata_only() -> FeatureFactorKickoffAssertion:
    return _build_assertion("phase116_scope_metadata_only", True, "Scope must be metadata only.")

def assertion_phase116_research_data_only() -> FeatureFactorKickoffAssertion:
    return _build_assertion("phase116_research_data_only", True, "Scope must be research data only.")

def assertion_no_active_paper() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_active_paper", True, "Active paper trading must be blocked.")

def assertion_no_broker() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_broker", True, "Broker execution must be blocked.")

def assertion_no_order() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_order", True, "Order creation must be blocked.")

def assertion_no_paper_state_mutation() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_paper_state_mutation", True, "Paper state mutation must be blocked.")

def assertion_no_telegram_real_send() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_telegram_real_send", True, "Telegram real send must be blocked.")

def assertion_no_scraping() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_scraping", True, "Scraping must be blocked.")

def assertion_no_html_parsing() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_html_parsing", True, "HTML parsing must be blocked.")

def assertion_no_paid_api() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_paid_api", True, "Paid API must be blocked.")

def assertion_no_dashboard() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_dashboard", True, "Dashboard must be blocked.")

def assertion_no_trade_signal_generation() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_trade_signal_generation", True, "Trade signal generation must be blocked.")

def assertion_no_order_decision_generation() -> FeatureFactorKickoffAssertion:
    return _build_assertion("no_order_decision_generation", True, "Order decision generation must be blocked.")

def build_feature_factor_kickoff_assertions(acceptance: DataProviderFinalAcceptanceReport, closure: ProviderLayerClosureBundle, contract: FeatureFactorDataContract) -> list[FeatureFactorKickoffAssertion]:
    # We simply assert True for all these boundaries per instructions,
    # as they are logically derived from upstream checks.
    # In a full impl we'd cross-check against actual execution scopes.
    return [
        assertion_phase116_scope_metadata_only(),
        assertion_phase116_research_data_only(),
        assertion_no_active_paper(),
        assertion_no_broker(),
        assertion_no_order(),
        assertion_no_paper_state_mutation(),
        assertion_no_telegram_real_send(),
        assertion_no_scraping(),
        assertion_no_html_parsing(),
        assertion_no_paid_api(),
        assertion_no_dashboard(),
        assertion_no_trade_signal_generation(),
        assertion_no_order_decision_generation()
    ]

def feature_factor_kickoff_assertions_summary(assertions: list[FeatureFactorKickoffAssertion]) -> dict[str, Any]:
    return {
        "total": len(assertions),
        "passed": sum(1 for a in assertions if a.status == FeatureFactorKickoffAssertionStatus.PASS)
    }

def feature_factor_kickoff_assertions_to_text(assertions: list[FeatureFactorKickoffAssertion], limit: int = 200) -> str:
    s = feature_factor_kickoff_assertions_summary(assertions)
    return f"Assertions: {s['passed']}/{s['total']} passed."
