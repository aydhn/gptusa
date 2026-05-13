import datetime
from typing import Any, Optional, List

from usa_signal_bot.core.enums import (
    TradabilityStatus,
    ExecutionRiskLevel,
    ExecutionGuardReason,
    BorrowabilityProxyStatus
)
from usa_signal_bot.execution.liquidity_models import (
    TradabilityGuardResult,
    BorrowabilityProxyResult,
    LiquidityProfile,
    create_tradability_guard_id
)
from usa_signal_bot.core.config_schema import BorrowabilityProxyConfig
from usa_signal_bot.execution.borrowability_proxy import estimate_borrowability_proxy

def short_trade_block_reasons(
    borrow_result: BorrowabilityProxyResult,
    liquidity_profile: LiquidityProfile | None = None
) -> list[ExecutionGuardReason]:
    reasons = []

    if borrow_result.status == BorrowabilityProxyStatus.LIKELY_UNAVAILABLE:
        reasons.append(ExecutionGuardReason.SHORT_BORROW_PROXY_RISK)
    elif borrow_result.status == BorrowabilityProxyStatus.REVIEW_REQUIRED:
        reasons.append(ExecutionGuardReason.DELISTING_OR_LIFECYCLE_RISK)

    if liquidity_profile:
        if liquidity_profile.avg_dollar_volume and liquidity_profile.avg_dollar_volume < 1_000_000:
            reasons.append(ExecutionGuardReason.LOW_DOLLAR_VOLUME)
        if liquidity_profile.last_price and liquidity_profile.last_price < 2.0:
            reasons.append(ExecutionGuardReason.LOW_PRICE)

    return list(set(reasons))

def should_block_short_signal(
    borrow_result: BorrowabilityProxyResult,
    liquidity_profile: LiquidityProfile | None = None,
    config: BorrowabilityProxyConfig | None = None
) -> bool:
    if config is None:
        config = BorrowabilityProxyConfig()

    if config.block_short_on_likely_unavailable and borrow_result.status == BorrowabilityProxyStatus.LIKELY_UNAVAILABLE:
        return True

    if config.require_review_on_hard_to_borrow_proxy and borrow_result.status == BorrowabilityProxyStatus.REVIEW_REQUIRED:
        # Depending on strictness, review might equal block in fully automated pipeline
        return True

    # Block penny stocks for shorting anyway as a heuristic
    if liquidity_profile and liquidity_profile.last_price and liquidity_profile.last_price < 2.0:
        return True

    return False

def evaluate_short_realism(
    symbol: str,
    rows: list[dict[str, Any]],
    notional_usd: float | None = None,
    lifecycle_metadata: dict[str, Any] | None = None,
    corporate_action_metadata: dict[str, Any] | None = None,
    liquidity_profile: LiquidityProfile | None = None,
    config: BorrowabilityProxyConfig | None = None
) -> TradabilityGuardResult:

    if config is None:
        config = BorrowabilityProxyConfig()

    borrow_result = estimate_borrowability_proxy(
        symbol, rows, liquidity_profile, lifecycle_metadata, corporate_action_metadata, config
    )

    reasons = short_trade_block_reasons(borrow_result, liquidity_profile)
    is_blocked = should_block_short_signal(borrow_result, liquidity_profile, config)

    status = TradabilityStatus.TRADABLE
    risk_level = ExecutionRiskLevel.LOW
    recommended_guards = []

    if is_blocked:
        status = TradabilityStatus.BLOCK_SIGNAL
        risk_level = ExecutionRiskLevel.CRITICAL
        recommended_guards.append("block_short_due_to_borrow_proxy")
    elif borrow_result.status in [BorrowabilityProxyStatus.LIKELY_HARD, BorrowabilityProxyStatus.REVIEW_REQUIRED]:
        status = TradabilityStatus.REVIEW_REQUIRED
        risk_level = ExecutionRiskLevel.HIGH
        recommended_guards.append("require_manual_review")
    elif borrow_result.status == BorrowabilityProxyStatus.LIKELY_NORMAL:
        status = TradabilityStatus.CAUTION
        risk_level = ExecutionRiskLevel.MODERATE

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    return TradabilityGuardResult(
        guard_id=create_tradability_guard_id(symbol),
        symbol=symbol,
        created_at_utc=now_utc,
        status=status,
        risk_level=risk_level,
        liquidity_profile=liquidity_profile,
        spread_estimate=None,
        slippage_estimate=None,
        reasons=reasons,
        recommended_guards=recommended_guards,
        warnings=borrow_result.warnings,
        errors=borrow_result.errors,
        metadata={"borrow_proxy_result": borrow_result.status.value}
    )

def short_realism_to_text(result: TradabilityGuardResult) -> str:
    lines = [
        f"Short Realism Guard for {result.symbol}:",
        f"  Status: {result.status.value}",
        f"  Risk Level: {result.risk_level.value}",
    ]
    if result.reasons:
        lines.append("  Reasons:")
        for r in result.reasons:
            lines.append(f"   - {r.value}")
    if result.recommended_guards:
        lines.append("  Recommended Guards:")
        for g in result.recommended_guards:
            lines.append(f"   - {g}")
    if result.warnings:
        lines.append("  Warnings:")
        for w in result.warnings:
            lines.append(f"   - {w}")
    lines.append("  Note: No real broker order is placed. This is a heuristic test.")
    return "\n".join(lines)
