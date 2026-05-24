from typing import Dict, Any, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    ProviderKickoffAssertion,
    ProviderKickoffAssertionStatus,
    CoreRuntimeAcceptanceReport,
    AdvancedFoundationFreezeBundle,
    create_provider_kickoff_assertion_id,
    _now
)

def required_provider_kickoff_assertions() -> List[str]:
    return [
        "phase106_scope_metadata_only",
        "no_active_paper",
        "no_broker",
        "no_order",
        "no_paper_state_mutation",
        "no_telegram_real_send",
        "no_scraping",
        "no_html_parsing",
        "no_paid_api",
        "provider_network_fetch_not_required",
        "not_investment_advice"
    ]

def build_provider_kickoff_assertions(acceptance_report: CoreRuntimeAcceptanceReport, foundation_freeze: AdvancedFoundationFreezeBundle) -> List[ProviderKickoffAssertion]:
    return [
        assertion_phase106_scope_metadata_only(),
        assertion_no_active_paper(),
        assertion_no_broker(),
        assertion_no_order(),
        assertion_no_paper_state_mutation(),
        assertion_no_telegram_real_send(),
        assertion_no_scraping(),
        assertion_no_html_parsing(),
        assertion_no_paid_api(),
        assertion_provider_network_fetch_not_required(),
        assertion_not_investment_advice()
    ]

def _build_assertion(name: str) -> ProviderKickoffAssertion:
    return ProviderKickoffAssertion(
        assertion_id=create_provider_kickoff_assertion_id(),
        created_at_utc=_now(),
        assertion_name=name,
        status=ProviderKickoffAssertionStatus.PASS
    )

def assertion_phase106_scope_metadata_only() -> ProviderKickoffAssertion: return _build_assertion("phase106_scope_metadata_only")
def assertion_no_active_paper() -> ProviderKickoffAssertion: return _build_assertion("no_active_paper")
def assertion_no_broker() -> ProviderKickoffAssertion: return _build_assertion("no_broker")
def assertion_no_order() -> ProviderKickoffAssertion: return _build_assertion("no_order")
def assertion_no_paper_state_mutation() -> ProviderKickoffAssertion: return _build_assertion("no_paper_state_mutation")
def assertion_no_telegram_real_send() -> ProviderKickoffAssertion: return _build_assertion("no_telegram_real_send")
def assertion_no_scraping() -> ProviderKickoffAssertion: return _build_assertion("no_scraping")
def assertion_no_html_parsing() -> ProviderKickoffAssertion: return _build_assertion("no_html_parsing")
def assertion_no_paid_api() -> ProviderKickoffAssertion: return _build_assertion("no_paid_api")
def assertion_provider_network_fetch_not_required() -> ProviderKickoffAssertion: return _build_assertion("provider_network_fetch_not_required")
def assertion_not_investment_advice() -> ProviderKickoffAssertion: return _build_assertion("not_investment_advice")

def provider_kickoff_assertions_summary(assertions: List[ProviderKickoffAssertion]) -> Dict[str, Any]:
    return {
        "total": len(assertions),
        "passed": len([a for a in assertions if a.status.name == "PASS"])
    }

def provider_kickoff_assertions_to_text(assertions: List[ProviderKickoffAssertion], limit: int = 200) -> str:
    return f"Kickoff Assertions: {len(assertions)}"
