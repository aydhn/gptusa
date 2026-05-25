from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.provider_cache.phase108_models import (
    FallbackDryRunPlan,
    create_fallback_dry_run_plan_id
)

def build_fallback_dry_run_plan(symbol: str, capability: str = "GET_DAILY_OHLCV", provider_kind: str = "MARKET_DATA", interval: str | None = "1d", primary_provider: str | None = "YFINANCE", fallback_chain: list[str] | None = None) -> FallbackDryRunPlan:
    if fallback_chain is None:
        fallback_chain = ["YFINANCE", "LOCAL_CSV", "STOOQ"]

    return FallbackDryRunPlan(
        plan_id=create_fallback_dry_run_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        provider_kind=provider_kind,
        capability=capability,
        symbol=symbol,
        interval=interval,
        primary_provider=primary_provider,
        fallback_chain=fallback_chain,
        cache_only=True,
        dry_run_only=True,
        allow_network=False,
        allow_paid_api=False,
        allow_scraping=False,
        allow_html_parsing=False,
        allow_broker=False,
        allow_order=False,
        allow_paper_mutation=False,
        expected_schema=["timestamp", "open", "high", "low", "close", "volume"],
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_default_fallback_dry_run_plans(symbols: list[str] | None = None) -> list[FallbackDryRunPlan]:
    if not symbols:
        symbols = ["AAPL", "MSFT", "SPY"]
    return [build_fallback_dry_run_plan(sym) for sym in symbols]

def validate_fallback_dry_run_plan_safety(plan: FallbackDryRunPlan) -> list[str]:
    errors = []
    if not plan.cache_only:
        errors.append("cache_only must be true")
    if not plan.dry_run_only:
        errors.append("dry_run_only must be true")
    if plan.allow_network:
        errors.append("allow_network must be false")
    if plan.allow_paid_api:
        errors.append("allow_paid_api must be false")
    if plan.allow_scraping:
        errors.append("allow_scraping must be false")
    if plan.allow_html_parsing:
        errors.append("allow_html_parsing must be false")
    if plan.allow_broker:
        errors.append("allow_broker must be false")
    if plan.allow_order:
        errors.append("allow_order must be false")
    if plan.allow_paper_mutation:
        errors.append("allow_paper_mutation must be false")
    return errors

def fallback_dry_run_plan_summary(plan: FallbackDryRunPlan) -> dict[str, Any]:
    return {"id": plan.plan_id, "symbol": plan.symbol}

def fallback_dry_run_plan_to_text(plan: FallbackDryRunPlan) -> str:
    return f"Fallback Plan {plan.plan_id} for {plan.symbol}"
