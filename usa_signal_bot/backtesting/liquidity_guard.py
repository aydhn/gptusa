from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    LiquidityGuard,
    create_liquidity_guard_id
)
from usa_signal_bot.core.enums import LiquidityGuardKind

def build_default_liquidity_guard() -> LiquidityGuard:
    return LiquidityGuard(
        guard_id=create_liquidity_guard_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        guard_kinds=[LiquidityGuardKind.MIN_DOLLAR_VOLUME, LiquidityGuardKind.MIN_PRICE, LiquidityGuardKind.MAX_VOLUME_PARTICIPATION],
        min_dollar_volume=1000000.0,
        min_share_volume=None,
        max_volume_participation=0.01,
        min_price=1.0,
        missing_volume_blocks_execution=True,
        guard_valid=True,
        order_creation_allowed=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_liquidity_guard(guard: LiquidityGuard) -> list[str]:
    errors = []
    if guard.order_creation_allowed:
        errors.append("order_creation_allowed must be False")
    return errors

def evaluate_liquidity_row(row: dict[str, Any], guard: LiquidityGuard) -> dict[str, Any]:
    price = row.get("close", row.get("price", 0.0))
    volume = row.get("volume", 0.0)
    dollar_vol = price * volume

    passed = True
    reasons = []

    if guard.min_dollar_volume is not None and dollar_vol < guard.min_dollar_volume:
        passed = False
        reasons.append("MIN_DOLLAR_VOLUME_FAILED")

    if guard.min_price is not None and price < guard.min_price:
        passed = False
        reasons.append("MIN_PRICE_FAILED")

    if guard.missing_volume_blocks_execution and volume <= 0:
        passed = False
        reasons.append("MISSING_VOLUME")

    return {"passed": passed, "reasons": reasons}

def liquidity_guard_summary(guard: LiquidityGuard) -> dict[str, Any]:
    return {"valid": guard.guard_valid, "kinds": [k.value for k in guard.guard_kinds]}

def liquidity_guard_to_text(guard: LiquidityGuard, limit: int = 300) -> str:
    return f"LiquidityGuard(valid={guard.guard_valid}, order_creation={guard.order_creation_allowed})"
