from pathlib import Path
from typing import Any, Optional, Dict, List
from datetime import datetime, timezone

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderFetchDryRunPlan,
    ProviderFetchDryRunResult,
    create_provider_fetch_dry_run_result_id
)
from usa_signal_bot.data_provider_runtime.cache_lookup_dry_run import run_cache_lookup_dry_run
from usa_signal_bot.core.enums import ProviderFetchDryRunStatus, ProviderCacheLookupStatus, ProviderRuntimeRiskFlag


def execute_fetch_dry_run(plan: ProviderFetchDryRunPlan, cache_root: Optional[Path] = None) -> ProviderFetchDryRunResult:
    result = ProviderFetchDryRunResult(
        result_id=create_provider_fetch_dry_run_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        plan_id=plan.plan_id,
        provider_name=plan.provider_name,
        status=ProviderFetchDryRunStatus.PLANNED,
        fetch_performed=False,
        network_used=False
    )

    errors = validate_fetch_dry_run_result_safety(result)
    if errors:
        result.status = ProviderFetchDryRunStatus.BLOCKED
        result.errors.extend(errors)
        return result

    if plan.errors:
        result.status = ProviderFetchDryRunStatus.BLOCKED
        result.errors.extend(plan.errors)
        return result

    if plan.cache_key and plan.allow_cache:
        lookup_res = run_cache_lookup_dry_run(plan.cache_key, cache_root)
        result.cache_lookup = lookup_res

        if lookup_res.status == ProviderCacheLookupStatus.CACHE_HIT:
            result.status = ProviderFetchDryRunStatus.CACHE_HIT_SIMULATED
            result.rows_returned = lookup_res.rows_available
            result.passed = True
            return result
        else:
            result.status = ProviderFetchDryRunStatus.CACHE_MISS_SIMULATED

    if not plan.allow_network:
        result.status = ProviderFetchDryRunStatus.FETCH_SKIPPED_NETWORK_DISABLED
        result.passed = True
        return result

    if plan.metadata_only or plan.dry_run_only:
        result.status = ProviderFetchDryRunStatus.FETCH_SKIPPED_DRY_RUN
        result.passed = True
        return result

    result.status = ProviderFetchDryRunStatus.BLOCKED
    result.errors.append("Unhandled execution path in fetch dry run")
    return result


def execute_fetch_dry_run_batch(plans: List[ProviderFetchDryRunPlan], cache_root: Optional[Path] = None) -> List[ProviderFetchDryRunResult]:
    results = []
    for plan in plans:
        results.append(execute_fetch_dry_run(plan, cache_root))
    return results

def validate_fetch_dry_run_result_safety(result: ProviderFetchDryRunResult) -> List[str]:
    errors = []
    if result.fetch_performed:
        errors.append("fetch_performed must be False")
    if result.network_used:
        errors.append("network_used must be False")
    if result.paid_api_used:
        errors.append("paid_api_used must be False")
    if result.scraping_used or result.html_parsing_used or result.broker_used or result.order_created or result.paper_state_mutated or result.telegram_real_sent or result.dashboard_started:
        errors.append("Unauthorized usage in fetch dry run")
    return errors


def fetch_dry_run_result_summary(result: ProviderFetchDryRunResult) -> Dict[str, Any]:
    return {
        "result_id": result.result_id,
        "plan_id": result.plan_id,
        "status": result.status.value,
        "passed": result.passed,
        "network_used": result.network_used
    }

def fetch_dry_run_result_to_text(result: ProviderFetchDryRunResult) -> str:
    lines = [
        "=== Provider Fetch Dry Run Result ===",
        f"ID: {result.result_id}",
        f"Status: {result.status.value}",
        f"Passed: {result.passed}",
        f"Network Used: {result.network_used}",
        ""
    ]
    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
