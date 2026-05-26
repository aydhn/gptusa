from typing import Any, Dict, List, Optional
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderFreezeContext,
    ProviderExpansionFreezeBundle
)
from usa_signal_bot.core.enums import ProviderFreezeRiskFlag

def freeze_text_has_trade_or_execution_language(text: str) -> bool:
    bad_phrases = [
        "emir gönderildi", "aktif trading başladı", "paper'a alındı",
        "canlıya alındı", "kesin al", "kesin sat", "garanti kâr",
        "buy signal", "sell signal", "strong buy", "strong sell", "sent_to_broker"
    ]
    t = text.lower()
    return any(p in t for p in bad_phrases)

def validate_provider_freeze_context_safety(context: ProviderFreezeContext) -> List[str]:
    errors = []
    if context.activation_allowed: errors.append("Context allows activation.")
    if context.active_paper_enabled: errors.append("Context allows active paper.")
    if context.broker_execution_enabled: errors.append("Context allows broker execution.")
    if context.order_creation_enabled: errors.append("Context allows order creation.")
    if context.paper_state_mutation_enabled: errors.append("Context allows paper mutation.")
    if context.telegram_real_send_enabled: errors.append("Context allows Telegram real send.")
    if context.scraping_enabled: errors.append("Context allows scraping.")
    if context.html_parse_enabled: errors.append("Context allows HTML parsing.")
    if context.paid_api_enabled: errors.append("Context allows paid API.")
    if context.dashboard_enabled: errors.append("Context allows dashboard.")
    if context.network_default_enabled: errors.append("Context allows network default.")

    if context.network_used: errors.append("Context indicates network used.")
    if context.order_created: errors.append("Context indicates order created.")
    if context.paper_state_mutated: errors.append("Context indicates paper mutated.")
    if context.produces_trade_signal: errors.append("Context indicates trade signals produced.")
    if context.produces_order_decision: errors.append("Context indicates order decision produced.")

    return errors

def validate_freeze_bundle_safety(bundle: ProviderExpansionFreezeBundle) -> List[str]:
    errors = []
    if bundle.secret_violation_count > 0: errors.append("Bundle contains secrets.")
    if bundle.execution_violation_count > 0: errors.append("Bundle contains execution language.")
    if bundle.trade_signal_violation_count > 0: errors.append("Bundle contains trade signals.")
    if bundle.order_decision_violation_count > 0: errors.append("Bundle contains order decisions.")
    return errors

def collect_provider_freeze_risk_flags(context: Optional[ProviderFreezeContext] = None) -> List[ProviderFreezeRiskFlag]:
    flags = set()
    if context:
        flags.update(context.risk_flags)
        flags.update(context.ingestion.risk_flags)
        flags.update(context.freeze_bundle.risk_flags)
        flags.update(context.multi_provider_review.risk_flags)
        flags.update(context.rehearsal_report.risk_flags)
        flags.update(context.output_contract.risk_flags)
        flags.update(context.artifact_manifest.risk_flags)
    return list(flags)

def freeze_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def freeze_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Provider Freeze Safety Validation Passed."
    return "Provider Freeze Safety Validation Errors:\n" + "\n".join(f" - {e}" for e in errors)
