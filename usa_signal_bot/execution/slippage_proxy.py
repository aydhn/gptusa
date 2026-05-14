import math
from typing import Any, Optional
from usa_signal_bot.core.enums import ExecutionRealismStatus, ExecutionRiskLevel
from usa_signal_bot.execution.liquidity_models import SlippageProxyEstimate, LiquidityProfile, create_slippage_proxy_estimate_id
from usa_signal_bot.core.config_schema import SpreadSlippageProxyConfig
import datetime

def estimate_slippage_proxy(
    symbol: str,
    rows: list[dict[str, Any]],
    side: str,
    notional_usd: float | None = None,
    liquidity_profile: LiquidityProfile | None = None,
    config: SpreadSlippageProxyConfig | None = None
) -> SlippageProxyEstimate:

    config = config or SpreadSlippageProxyConfig()

    _id = create_slippage_proxy_estimate_id(symbol)
    _now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if notional_usd is None:
        return SlippageProxyEstimate(estimate_id=_id, symbol=symbol, created_at_utc=_now, side=side, notional_usd=None, participation_rate_pct=None, slippage_proxy_bps=None, status=ExecutionRealismStatus.INSUFFICIENT_DATA, risk_level=ExecutionRiskLevel.UNKNOWN, warnings=[], errors=["Missing notional"])

    adv = liquidity_profile.avg_dollar_volume if liquidity_profile else None
    if adv is None or adv <= 0:
        return SlippageProxyEstimate(estimate_id=_id, symbol=symbol, created_at_utc=_now, side=side, notional_usd=notional_usd, participation_rate_pct=None, slippage_proxy_bps=None, status=ExecutionRealismStatus.INSUFFICIENT_DATA, risk_level=ExecutionRiskLevel.UNKNOWN, warnings=[], errors=["Missing ADV"])

    participation = (notional_usd / adv) * 100.0

    # Heuristic slippage
    bps = 5.0
    if participation > 1.0:
        bps += (participation - 1.0) * 10.0

    status = ExecutionRealismStatus.REALISTIC
    if participation > 10.0:
        status = ExecutionRealismStatus.UNREALISTIC

    return SlippageProxyEstimate(
        estimate_id=_id,
        symbol=symbol,
        created_at_utc=_now,
        side=side,
        notional_usd=notional_usd,
        participation_rate_pct=participation,
        slippage_proxy_bps=bps,
        status=status,
        risk_level=ExecutionRiskLevel.LOW if status == ExecutionRealismStatus.REALISTIC else ExecutionRiskLevel.HIGH,
        warnings=[],
        errors=[]
    )

def slippage_proxy_to_text(estimate: SlippageProxyEstimate) -> str:
    lines = [
        f"Slippage Proxy Estimate ({estimate.symbol}):",
        f"  Side: {estimate.side}",
        f"  Participation Rate: {estimate.participation_rate_pct:.4f}%" if estimate.participation_rate_pct is not None else "  Participation Rate: Unknown",
        f"  Estimated Slippage: {estimate.slippage_proxy_bps:.2f} bps" if getattr(estimate, 'slippage_proxy_bps', None) is not None else "  Estimated Slippage: Unknown",
        f"  Status: {estimate.status.value if isinstance(estimate.status, ExecutionRealismStatus) else estimate.status}"
    ]
    if estimate.warnings:
        lines.append("  Warnings:")
        for w in estimate.warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines)
