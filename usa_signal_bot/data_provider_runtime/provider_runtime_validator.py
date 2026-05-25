from typing import Any, Dict, List

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderRuntimeContext,
    ProviderRuntimeAdapterSpec,
    ProviderFetchDryRunResult
)
from usa_signal_bot.core.enums import ProviderRuntimeRiskFlag


def validate_provider_runtime_context_safety(context: ProviderRuntimeContext) -> List[str]:
    errors = []

    if not context.ingestion.provider_abstraction_ready:
        errors.append("provider_abstraction_ready must be True")
    if not context.ingestion.metadata_only:
        errors.append("ingestion metadata_only must be True")
    if context.ingestion.provider_network_fetch_enabled_now:
        errors.append("provider_network_fetch_enabled_now must be False")

    if context.network_enabled_by_default:
        errors.append("network_enabled_by_default must be False")
    if context.paid_api_enabled:
        errors.append("paid_api_enabled must be False")
    if context.scraping_enabled:
        errors.append("scraping_enabled must be False")
    if context.html_parse_enabled:
        errors.append("html_parse_enabled must be False")
    if context.broker_execution_enabled:
        errors.append("broker_execution_enabled must be False")
    if context.order_creation_enabled:
        errors.append("order_creation_enabled must be False")
    if context.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled must be False")
    if context.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled must be False")
    if context.dashboard_enabled:
        errors.append("dashboard_enabled must be False")

    return errors

def validate_provider_runtime_adapter_specs(specs: List[ProviderRuntimeAdapterSpec]) -> List[str]:
    errors = []
    for spec in specs:
        if spec.network_enabled_by_default:
            errors.append(f"{spec.provider_name} has network_enabled_by_default=True")
        if spec.paid_api:
            errors.append(f"{spec.provider_name} has paid_api=True")
        if spec.scraping_required:
            errors.append(f"{spec.provider_name} has scraping_required=True")
        if spec.html_parsing_required:
            errors.append(f"{spec.provider_name} has html_parsing_required=True")
        if spec.credential_required_now:
            errors.append(f"{spec.provider_name} has credential_required_now=True")
        if spec.broker_related or spec.order_related or spec.paper_mutation_related:
            errors.append(f"{spec.provider_name} is broker/order/mutation related")
    return errors

def validate_provider_dry_run_results(results: List[ProviderFetchDryRunResult]) -> List[str]:
    errors = []
    for res in results:
        if res.fetch_performed:
            errors.append(f"{res.provider_name} fetch_performed must be False")
        if res.network_used:
            errors.append(f"{res.provider_name} network_used must be False")
        if res.paid_api_used:
            errors.append(f"{res.provider_name} paid_api_used must be False")
        if res.scraping_used or res.html_parsing_used or res.broker_used or res.order_created or res.paper_state_mutated or res.telegram_real_sent or res.dashboard_started:
            errors.append(f"{res.provider_name} unauthorized usage in fetch dry run")
    return errors

def collect_provider_runtime_risk_flags(context: ProviderRuntimeContext | None = None) -> List[ProviderRuntimeRiskFlag]:
    flags = set()
    if context:
        flags.update(context.ingestion.risk_flags)
        for spec in context.adapter_specs:
            flags.update(spec.risk_flags)
        for plan in context.dry_run_plans:
            flags.update(plan.risk_flags)
        for res in context.dry_run_results:
            flags.update(res.risk_flags)
        flags.update(context.contract_test_report.risk_flags)
    return list(flags)

def provider_runtime_validator_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def provider_runtime_validator_to_text(errors: List[str]) -> str:
    lines = [
        "=== Provider Runtime Validator ===",
        f"Valid: {len(errors) == 0}",
        ""
    ]
    if errors:
        lines.append("Errors:")
        for e in errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
