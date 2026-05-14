from typing import Any
from usa_signal_bot.core.enums import ExecutionGuardReason
from usa_signal_bot.execution.liquidity_models import LiquidityProfile

class ShortRealismResult:
    def __init__(self, reasons: list[ExecutionGuardReason]):
        self.reasons = reasons

def evaluate_short_realism(
    symbol: str,
    rows: list[dict[str, Any]],
    notional_usd: float | None = None,
    lifecycle_metadata: dict[str, Any] | None = None,
    corporate_action_metadata: dict[str, Any] | None = None,
    liquidity_profile: LiquidityProfile | None = None
) -> ShortRealismResult:

    reasons = []

    if liquidity_profile:
        if liquidity_profile.avg_dollar_volume and liquidity_profile.avg_dollar_volume < 1000000:
            reasons.append(ExecutionGuardReason.SHORT_BORROW_PROXY_RISK)

    return ShortRealismResult(reasons)
