import datetime
from typing import Any, Optional

from usa_signal_bot.core.enums import ExecutionRealismStatus
from usa_signal_bot.execution.liquidity_models import (
    LiquidityProfile,
    SpreadProxyEstimate,
    create_spread_proxy_estimate_id
)
from usa_signal_bot.core.config_schema import SpreadSlippageProxyConfig

def estimate_spread_proxy_bps_from_ohlcv(
    rows: list[dict[str, Any]],
    liquidity_profile: LiquidityProfile | None = None,
    config: SpreadSlippageProxyConfig | None = None
) -> float | None:
    if not rows:
        return None

    if config is None:
        config = SpreadSlippageProxyConfig()

    # Base spread proxy logic (heuristic)
    base_bps = 5.0 # Very liquid default

    if liquidity_profile:
        addv = liquidity_profile.avg_dollar_volume
        if addv is not None:
            if addv > 100_000_000:
                base_bps = 2.0
            elif addv < 1_000_000:
                base_bps = 50.0
            elif addv < 5_000_000:
                base_bps = 25.0

        price = liquidity_profile.last_price
        if price is not None and config.use_low_price_penalty:
            if price < 1.0:
                base_bps += 100.0
            elif price < 5.0:
                base_bps += 50.0

        atr_pct = liquidity_profile.atr_pct
        if atr_pct is not None and config.use_atr_penalty:
            if atr_pct > 5.0:
                base_bps += 20.0
            elif atr_pct > 10.0:
                base_bps += 50.0

    return base_bps

def classify_spread_proxy_status(
    spread_bps: float | None,
    config: SpreadSlippageProxyConfig | None = None
) -> ExecutionRealismStatus:
    if spread_bps is None:
        return ExecutionRealismStatus.INSUFFICIENT_DATA

    if config is None:
        config = SpreadSlippageProxyConfig()

    if spread_bps > config.high_spread_proxy_bps:
        return ExecutionRealismStatus.UNREALISTIC
    if spread_bps > config.max_spread_proxy_bps:
        return ExecutionRealismStatus.ACCEPTABLE_WITH_WARNINGS

    return ExecutionRealismStatus.REALISTIC

def estimate_spread_proxy(
    symbol: str,
    rows: list[dict[str, Any]],
    liquidity_profile: LiquidityProfile | None = None,
    config: SpreadSlippageProxyConfig | None = None
) -> SpreadProxyEstimate:

    if config is None:
        config = SpreadSlippageProxyConfig()

    spread_bps = estimate_spread_proxy_bps_from_ohlcv(rows, liquidity_profile, config)
    status = classify_spread_proxy_status(spread_bps, config)

    warnings = []
    if status == ExecutionRealismStatus.UNREALISTIC:
        warnings.append("Spread proxy is extremely high, indicating high execution risk.")
    elif status == ExecutionRealismStatus.ACCEPTABLE_WITH_WARNINGS:
        warnings.append("Spread proxy is elevated.")

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    estimate = SpreadProxyEstimate(
        estimate_id=create_spread_proxy_estimate_id(symbol),
        symbol=symbol,
        created_at_utc=now_utc,
        spread_proxy_bps=spread_bps,
        method="heuristic_from_ohlcv",
        status=status,
        warnings=warnings,
        errors=[],
        metadata={}
    )

    return estimate

def spread_proxy_to_text(estimate: SpreadProxyEstimate) -> str:
    lines = [
        f"Spread Proxy Estimate for {estimate.symbol}:",
        f"  Status: {estimate.status.value}",
        f"  Spread Proxy (bps): {estimate.spread_proxy_bps}",
    ]
    if estimate.warnings:
        lines.append("  Warnings:")
        for w in estimate.warnings:
            lines.append(f"   - {w}")
    lines.append("  Note: This is a heuristic proxy, not an actual bid/ask spread.")
    return "\n".join(lines)
