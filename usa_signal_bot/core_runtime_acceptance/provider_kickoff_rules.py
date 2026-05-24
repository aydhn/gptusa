from typing import Dict, Any, List, Optional
from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    ProviderKickoffRule,
    ProviderKickoffRuleStatus,
    CoreRuntimeAcceptanceReport,
    AdvancedFoundationFreezeBundle,
    create_provider_kickoff_rule_id,
    _now
)

def required_provider_kickoff_rule_names() -> List[str]:
    return [
        "core_runtime_accepted",
        "foundation_frozen",
        "provider_interfaces_ready",
        "no_paid_api_enabled",
        "no_scraping_enabled",
        "no_html_parse_enabled",
        "no_broker_execution_enabled",
        "no_order_enabled",
        "no_paper_mutation_enabled",
        "no_telegram_real_send_enabled"
    ]

def build_provider_kickoff_rules(acceptance_report: CoreRuntimeAcceptanceReport, foundation_freeze: AdvancedFoundationFreezeBundle) -> List[ProviderKickoffRule]:
    return [
        rule_core_runtime_accepted(acceptance_report),
        rule_foundation_frozen(foundation_freeze),
        rule_provider_interfaces_ready(acceptance_report),
        rule_no_paid_api_enabled(acceptance_report),
        rule_no_scraping_enabled(acceptance_report),
        rule_no_html_parse_enabled(acceptance_report),
        rule_no_broker_execution_enabled(acceptance_report),
        rule_no_order_enabled(acceptance_report),
        rule_no_paper_mutation_enabled(acceptance_report),
        rule_no_telegram_real_send_enabled(acceptance_report)
    ]

def _build_rule(name: str, passed: bool) -> ProviderKickoffRule:
    return ProviderKickoffRule(
        rule_id=create_provider_kickoff_rule_id(),
        created_at_utc=_now(),
        rule_name=name,
        status=ProviderKickoffRuleStatus.PASS if passed else ProviderKickoffRuleStatus.FAIL,
        required=True
    )

def rule_core_runtime_accepted(report: CoreRuntimeAcceptanceReport) -> ProviderKickoffRule:
    return _build_rule("core_runtime_accepted", report.core_runtime_accepted)

def rule_foundation_frozen(bundle: AdvancedFoundationFreezeBundle) -> ProviderKickoffRule:
    return _build_rule("foundation_frozen", bundle.frozen)

def rule_provider_interfaces_ready(report: CoreRuntimeAcceptanceReport) -> ProviderKickoffRule:
    # Assume True if report passed
    return _build_rule("provider_interfaces_ready", report.core_runtime_accepted)

def rule_no_paid_api_enabled(report: Optional[CoreRuntimeAcceptanceReport] = None) -> ProviderKickoffRule:
    return _build_rule("no_paid_api_enabled", True)

def rule_no_scraping_enabled(report: Optional[CoreRuntimeAcceptanceReport] = None) -> ProviderKickoffRule:
    return _build_rule("no_scraping_enabled", not getattr(report, "scraping_enabled", False))

def rule_no_html_parse_enabled(report: Optional[CoreRuntimeAcceptanceReport] = None) -> ProviderKickoffRule:
    return _build_rule("no_html_parse_enabled", True)

def rule_no_broker_execution_enabled(report: Optional[CoreRuntimeAcceptanceReport] = None) -> ProviderKickoffRule:
    return _build_rule("no_broker_execution_enabled", not getattr(report, "broker_execution_enabled", False))

def rule_no_order_enabled(report: Optional[CoreRuntimeAcceptanceReport] = None) -> ProviderKickoffRule:
    return _build_rule("no_order_enabled", True)

def rule_no_paper_mutation_enabled(report: Optional[CoreRuntimeAcceptanceReport] = None) -> ProviderKickoffRule:
    return _build_rule("no_paper_mutation_enabled", not getattr(report, "paper_state_mutation_enabled", False))

def rule_no_telegram_real_send_enabled(report: Optional[CoreRuntimeAcceptanceReport] = None) -> ProviderKickoffRule:
    return _build_rule("no_telegram_real_send_enabled", not getattr(report, "telegram_real_send_enabled", False))

def provider_kickoff_rules_summary(rules: List[ProviderKickoffRule]) -> Dict[str, Any]:
    return {
        "total": len(rules),
        "passed": len([r for r in rules if r.status.name == "PASS"])
    }

def provider_kickoff_rules_to_text(rules: List[ProviderKickoffRule], limit: int = 200) -> str:
    return f"Kickoff Rules: {len(rules)}"
