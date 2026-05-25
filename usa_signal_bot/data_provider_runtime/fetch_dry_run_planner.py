from typing import Any, Optional, Dict, List
from datetime import datetime, timezone

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderFetchDryRunPlan,
    create_provider_fetch_dry_run_plan_id,
    ProviderCacheKey
)
from usa_signal_bot.data_provider_runtime.cache_key_builder import build_provider_cache_key
from usa_signal_bot.core.enums import ProviderFetchMode, ProviderRuntimeRiskFlag


def build_fetch_dry_run_plan(
    provider_name: str,
    capability: str,
    symbol: Optional[str] = None,
    interval: Optional[str] = "1d",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fetch_mode: ProviderFetchMode = ProviderFetchMode.METADATA_ONLY,
    allow_cache: bool = True,
    allow_network: bool = False
) -> ProviderFetchDryRunPlan:

    plan = ProviderFetchDryRunPlan(
        plan_id=create_provider_fetch_dry_run_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        provider_name=provider_name,
        capability=capability,
        symbol=symbol,
        interval=interval,
        start_date=start_date,
        end_date=end_date,
        fetch_mode=fetch_mode,
        metadata_only=True,
        dry_run_only=True,
        allow_cache=allow_cache,
        allow_network=allow_network,
        allow_paid_api=False,
        allow_scraping=False,
        allow_html_parsing=False,
        allow_broker=False,
        allow_order=False,
        expected_schema=["symbol", "timestamp", "open", "high", "low", "close", "adjusted_close", "volume", "source", "fetched_at_utc"]
    )

    try:
        cache_key = build_provider_cache_key(
            provider_name=provider_name,
            capability=capability,
            symbol=symbol,
            interval=interval,
            start_date=start_date,
            end_date=end_date,
            adjusted=True,
            cache_namespace="market_data"
        )
        plan.cache_key = cache_key
    except Exception as e:
        plan.warnings.append(f"Failed to build cache key: {str(e)}")

    errors = validate_fetch_dry_run_plan_safety(plan)
    if errors:
        plan.errors.extend(errors)
        plan.risk_flags.append(ProviderRuntimeRiskFlag.NETWORK_FETCH_ATTEMPTED)

    return plan

def build_default_market_data_dry_run_plans(symbols: Optional[List[str]] = None) -> List[ProviderFetchDryRunPlan]:
    if not symbols:
        symbols = ["AAPL", "MSFT", "SPY"]

    plans = []
    for symbol in symbols:
        plans.append(build_fetch_dry_run_plan(
            provider_name="YFINANCE",
            capability="GET_DAILY_OHLCV",
            symbol=symbol,
            allow_network=False
        ))
    return plans

def validate_fetch_dry_run_plan_safety(plan: ProviderFetchDryRunPlan) -> List[str]:
    errors = []
    if not plan.dry_run_only:
        errors.append("dry_run_only must be True")
    if plan.allow_network:
        errors.append("allow_network must be False by default in dry run plan")
    if plan.allow_paid_api:
        errors.append("allow_paid_api must be False")
    if plan.allow_scraping:
        errors.append("allow_scraping must be False")
    if plan.allow_html_parsing:
        errors.append("allow_html_parsing must be False")
    if plan.allow_broker:
        errors.append("allow_broker must be False")
    if plan.allow_order:
        errors.append("allow_order must be False")
    return errors

def fetch_dry_run_plan_summary(plan: ProviderFetchDryRunPlan) -> Dict[str, Any]:
    return {
        "plan_id": plan.plan_id,
        "provider": plan.provider_name,
        "symbol": plan.symbol,
        "allow_network": plan.allow_network
    }

def fetch_dry_run_plan_to_text(plan: ProviderFetchDryRunPlan) -> str:
    lines = [
        "=== Provider Fetch Dry Run Plan ===",
        f"ID: {plan.plan_id}",
        f"Provider: {plan.provider_name}",
        f"Symbol: {plan.symbol}",
        f"Allow Network: {plan.allow_network}",
        ""
    ]
    if plan.errors:
        lines.append("Errors:")
        for e in plan.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
