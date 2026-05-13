import datetime
from typing import Any, Optional, Tuple

from usa_signal_bot.core.enums import ExecutionRealismStatus, ExecutionRiskLevel
from usa_signal_bot.execution.liquidity_models import (
    LiquidityProfile,
    SlippageProxyEstimate,
    create_slippage_proxy_estimate_id
)
from usa_signal_bot.core.config_schema import SpreadSlippageProxyConfig
from usa_signal_bot.execution.spread_proxy import estimate_spread_proxy_bps_from_ohlcv
from usa_signal_bot.execution.volume_participation import calculate_participation_rate_pct

def estimate_slippage_bps_from_liquidity(
    profile: LiquidityProfile,
    participation_rate_pct: float | None = None,
    spread_bps: float | None = None,
    config: SpreadSlippageProxyConfig | None = None
) -> float | None:
    if config is None:
        config = SpreadSlippageProxyConfig()

    if spread_bps is None:
        # Fallback if spread not passed
        base_spread = 5.0
    else:
        base_spread = spread_bps

    # Heuristic: Slippage is roughly half the spread for small orders + market impact
    slippage = base_spread / 2.0

    if participation_rate_pct is not None:
        if participation_rate_pct > 1.0:
            slippage += 10.0 * participation_rate_pct

    if profile.atr_pct is not None and config.use_atr_penalty:
        if profile.atr_pct > 5.0:
            slippage += 15.0

    if profile.last_price is not None and config.use_low_price_penalty:
        if profile.last_price < 2.0:
            slippage += 50.0

    return slippage

def classify_slippage_status(
    slippage_bps: float | None,
    participation_rate_pct: float | None = None,
    config: SpreadSlippageProxyConfig | None = None
) -> Tuple[ExecutionRealismStatus, ExecutionRiskLevel]:
    if slippage_bps is None:
        return ExecutionRealismStatus.INSUFFICIENT_DATA, ExecutionRiskLevel.UNKNOWN

    if config is None:
        config = SpreadSlippageProxyConfig()

    if slippage_bps > config.high_slippage_proxy_bps or (participation_rate_pct and participation_rate_pct > 10.0):
        return ExecutionRealismStatus.UNREALISTIC, ExecutionRiskLevel.CRITICAL

    if slippage_bps > config.max_slippage_proxy_bps or (participation_rate_pct and participation_rate_pct > 5.0):
        return ExecutionRealismStatus.ACCEPTABLE_WITH_WARNINGS, ExecutionRiskLevel.HIGH

    if participation_rate_pct and participation_rate_pct > 1.0:
        return ExecutionRealismStatus.REALISTIC, ExecutionRiskLevel.MODERATE

    return ExecutionRealismStatus.REALISTIC, ExecutionRiskLevel.LOW

def estimate_slippage_proxy(
    symbol: str,
    rows: list[dict[str, Any]],
    side: str = "long",
    notional_usd: float | None = None,
    liquidity_profile: LiquidityProfile | None = None,
    config: SpreadSlippageProxyConfig | None = None
) -> SlippageProxyEstimate:

    if config is None:
        config = SpreadSlippageProxyConfig()

    spread_bps = estimate_spread_proxy_bps_from_ohlcv(rows, liquidity_profile, config)

    participation_rate = None
    if notional_usd is not None and liquidity_profile is not None:
        participation_rate = calculate_participation_rate_pct(notional_usd, liquidity_profile.avg_dollar_volume)

    slippage_bps = None
    status = ExecutionRealismStatus.INSUFFICIENT_DATA
    risk = ExecutionRiskLevel.UNKNOWN

    if liquidity_profile is not None:
        slippage_bps = estimate_slippage_bps_from_liquidity(
            liquidity_profile, participation_rate, spread_bps, config
        )
        status, risk = classify_slippage_status(slippage_bps, participation_rate, config)

    warnings = []
    if status == ExecutionRealismStatus.UNREALISTIC:
        warnings.append("Slippage proxy is critically high.")
    elif status == ExecutionRealismStatus.ACCEPTABLE_WITH_WARNINGS:
        warnings.append("Slippage proxy is elevated.")

    if side.lower() == "short":
        warnings.append("Short side slippage might be exacerbated by borrow costs.")

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    return SlippageProxyEstimate(
        estimate_id=create_slippage_proxy_estimate_id(symbol),
        symbol=symbol,
        created_at_utc=now_utc,
        side=side,
        notional_usd=notional_usd,
        participation_rate_pct=participation_rate,
        slippage_proxy_bps=slippage_bps,
        status=status,
        risk_level=risk,
        warnings=warnings,
        errors=[],
        metadata={}
    )

def slippage_proxy_to_text(estimate: SlippageProxyEstimate) -> str:
    lines = [
        f"Slippage Proxy Estimate for {estimate.symbol} ({estimate.side}):",
        f"  Status: {estimate.status.value}",
        f"  Risk Level: {estimate.risk_level.value}",
        f"  Slippage Proxy (bps): {estimate.slippage_proxy_bps}",
        f"  Participation Rate: {estimate.participation_rate_pct}%" if estimate.participation_rate_pct else "  Participation Rate: Unknown"
    ]
    if estimate.warnings:
        lines.append("  Warnings:")
        for w in estimate.warnings:
            lines.append(f"   - {w}")
    lines.append("  Note: This is a heuristic proxy, not a guaranteed execution cost.")
    return "\n".join(lines)
