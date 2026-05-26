from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    FeatureFactorAllowedScope,
    FeatureFactorBlockedScope
)

def phase116_allowed_scopes() -> list[FeatureFactorAllowedScope]:
    return [
        FeatureFactorAllowedScope.INDICATOR_INPUT_CONTRACTS,
        FeatureFactorAllowedScope.FEATURE_SCHEMA_DEFINITIONS,
        FeatureFactorAllowedScope.FACTOR_METADATA_DEFINITIONS,
        FeatureFactorAllowedScope.OHLCV_FEATURE_FIXTURES,
        FeatureFactorAllowedScope.EVENT_CONTEXT_FEATURE_METADATA,
        FeatureFactorAllowedScope.CALENDAR_AWARE_FEATURE_METADATA,
        FeatureFactorAllowedScope.QUALITY_AWARE_FEATURE_METADATA,
        FeatureFactorAllowedScope.LOCAL_FEATURE_CACHE_PLAN,
        FeatureFactorAllowedScope.FEATURE_VALIDATION_RULES,
        FeatureFactorAllowedScope.FEATURE_LINEAGE_METADATA
    ]

def phase116_blocked_scopes() -> list[FeatureFactorBlockedScope]:
    return [
        FeatureFactorBlockedScope.TRADE_SIGNAL_GENERATION,
        FeatureFactorBlockedScope.STRATEGY_ACTIVATION,
        FeatureFactorBlockedScope.ORDER_DECISION,
        FeatureFactorBlockedScope.BROKER_EXECUTION,
        FeatureFactorBlockedScope.PAPER_STATE_MUTATION,
        FeatureFactorBlockedScope.LIVE_TRADING,
        FeatureFactorBlockedScope.DEMO_TRADING,
        FeatureFactorBlockedScope.TELEGRAM_REAL_SEND,
        FeatureFactorBlockedScope.DASHBOARD,
        FeatureFactorBlockedScope.PAID_API,
        FeatureFactorBlockedScope.SCRAPING,
        FeatureFactorBlockedScope.HTML_PARSING
    ]

def validate_phase116_scope_safety(allowed: list[FeatureFactorAllowedScope], blocked: list[FeatureFactorBlockedScope]) -> list[str]:
    errors = []
    expected_blocked = phase116_blocked_scopes()
    for exp in expected_blocked:
        if exp not in blocked:
            errors.append(f"Missing required blocked scope: {exp.value}")
    return errors

def phase116_scope_summary() -> dict[str, Any]:
    return {
        "allowed_count": len(phase116_allowed_scopes()),
        "blocked_count": len(phase116_blocked_scopes())
    }

def phase116_scope_to_text() -> str:
    s = phase116_scope_summary()
    return f"Scope: {s['allowed_count']} allowed, {s['blocked_count']} blocked."
