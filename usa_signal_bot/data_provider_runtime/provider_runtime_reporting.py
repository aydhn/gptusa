from typing import Any, Dict

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderAbstractionIngestionResult,
    ProviderRuntimeAdapterSpec,
    ProviderCacheKey,
    ProviderCacheLookupResult,
    ProviderFetchDryRunPlan,
    ProviderFetchDryRunResult,
    ProviderContractTestItem,
    ProviderContractTestReport,
    ProviderRuntimeContext,
    ProviderRuntimeFullReview
)

from usa_signal_bot.data_provider_runtime.provider_abstraction_ingestion import provider_abstraction_ingestion_to_text
from usa_signal_bot.data_provider_runtime.cache_key_builder import provider_cache_key_to_text
from usa_signal_bot.data_provider_runtime.cache_lookup_dry_run import cache_lookup_dry_run_to_text
from usa_signal_bot.data_provider_runtime.fetch_dry_run_planner import fetch_dry_run_plan_to_text
from usa_signal_bot.data_provider_runtime.fetch_dry_run_executor import fetch_dry_run_result_to_text
from usa_signal_bot.data_provider_runtime.provider_runtime_report import (
    provider_runtime_full_review_to_text,
    provider_runtime_limitations_text
)


def provider_abstraction_ingestion_result_to_text(item: ProviderAbstractionIngestionResult) -> str:
    return provider_abstraction_ingestion_to_text(item)

def provider_runtime_adapter_spec_to_text(item: ProviderRuntimeAdapterSpec) -> str:
    lines = [
        "=== Provider Runtime Adapter Spec ===",
        f"Provider Name: {item.provider_name}",
        f"Adapter Class: {item.adapter_class}",
        f"Implementation Status: {item.implementation_status.value}",
        f"Network Enabled by Default: {item.network_enabled_by_default}",
        ""
    ]
    if item.errors:
        lines.append("Errors:")
        for e in item.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)

def provider_contract_test_item_to_text(item: ProviderContractTestItem) -> str:
    return f"{item.test_name} ({item.adapter_class}): {item.status.value} - {item.message}"

def provider_contract_test_report_to_text(item: ProviderContractTestReport, limit: int = 200) -> str:
    lines = [
        "=== Provider Contract Test Report ===",
        f"Report ID: {item.report_id}",
        f"Status: {item.status.value}",
        f"Passed Tests: {item.passed_tests} / {item.total_tests}",
        f"Failed Tests: {item.failed_tests}",
        f"Blocked Tests: {item.blocked_tests}",
        f"Contract Tests Passed: {item.contract_tests_passed}",
        ""
    ]
    for i in item.items[:limit]:
        lines.append(provider_contract_test_item_to_text(i))
    if len(item.items) > limit:
        lines.append(f"... and {len(item.items) - limit} more")
    return "\n".join(lines)

def provider_runtime_context_to_text(item: ProviderRuntimeContext, limit: int = 300) -> str:
    lines = [
        "=== Provider Runtime Context ===",
        f"Context ID: {item.context_id}",
        f"Status: {item.status.value}",
        f"Adapter Count: {len(item.adapter_specs)}",
        f"Contract Tests Passed: {item.contract_test_report.contract_tests_passed}",
        ""
    ]
    if item.errors:
        lines.append("Errors:")
        for e in item.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)

def provider_runtime_store_summary_to_text(summary: Dict[str, Any]) -> str:
    lines = [
        "=== Provider Runtime Store Summary ===",
        f"Contexts Count: {summary.get('contexts_count', 0)}",
        f"Reviews Count: {summary.get('reviews_count', 0)}",
        ""
    ]
    return "\n".join(lines)
