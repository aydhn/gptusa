import datetime
from typing import Any, Optional, List

from usa_signal_bot.core.enums import (
    BorrowabilityProxyStatus,
    ExecutionRiskLevel,
    ExecutionGuardReason,
    SymbolLifecycleStatus
)
from usa_signal_bot.execution.liquidity_models import (
    LiquidityProfile,
    BorrowabilityProxyResult,
    create_borrowability_proxy_id
)
from usa_signal_bot.core.config_schema import BorrowabilityProxyConfig

def calculate_borrowability_proxy_score(
    symbol: str,
    rows: list[dict[str, Any]],
    liquidity_profile: LiquidityProfile | None = None,
    lifecycle_metadata: dict[str, Any] | None = None,
    corporate_action_metadata: dict[str, Any] | None = None,
    config: BorrowabilityProxyConfig | None = None
) -> float | None:
    if config is None:
        config = BorrowabilityProxyConfig()

    score = 100.0 # Start with assumption of easy to borrow

    if liquidity_profile:
        addv = liquidity_profile.avg_dollar_volume
        if addv is not None and config.low_liquidity_penalty:
            if addv < 1_000_000:
                score -= 40.0
            elif addv < 5_000_000:
                score -= 20.0

        price = liquidity_profile.last_price
        if price is not None and config.low_price_penalty:
            if price < 1.0:
                score -= 50.0
            elif price < 5.0:
                score -= 30.0

        atr = liquidity_profile.atr_pct
        if atr is not None and config.high_volatility_penalty:
            if atr > 10.0:
                score -= 20.0
            elif atr > 5.0:
                score -= 10.0

    if lifecycle_metadata and config.lifecycle_risk_penalty:
        status_val = lifecycle_metadata.get("status")
        if status_val in ["DELISTED", "SUSPENDED"]:
            score -= 100.0
        elif status_val == "REVIEW_REQUIRED":
            score -= 50.0

    if corporate_action_metadata and config.corporate_action_risk_penalty:
        if corporate_action_metadata.get("recent_split", False) or corporate_action_metadata.get("recent_merger", False):
            score -= 30.0

    return max(0.0, min(100.0, score))

def classify_borrowability_proxy(
    score: float | None,
    reasons: list[ExecutionGuardReason]
) -> BorrowabilityProxyStatus:
    if score is None:
        return BorrowabilityProxyStatus.UNKNOWN

    if ExecutionGuardReason.DELISTING_OR_LIFECYCLE_RISK in reasons:
        return BorrowabilityProxyStatus.REVIEW_REQUIRED

    if score >= 80.0:
        return BorrowabilityProxyStatus.LIKELY_EASY
    if score >= 60.0:
        return BorrowabilityProxyStatus.LIKELY_NORMAL
    if score >= 30.0:
        return BorrowabilityProxyStatus.LIKELY_HARD

    return BorrowabilityProxyStatus.LIKELY_UNAVAILABLE

def estimate_borrowability_proxy(
    symbol: str,
    rows: list[dict[str, Any]],
    liquidity_profile: LiquidityProfile | None = None,
    lifecycle_metadata: dict[str, Any] | None = None,
    corporate_action_metadata: dict[str, Any] | None = None,
    config: BorrowabilityProxyConfig | None = None
) -> BorrowabilityProxyResult:

    if config is None:
        config = BorrowabilityProxyConfig()

    score = calculate_borrowability_proxy_score(
        symbol, rows, liquidity_profile, lifecycle_metadata, corporate_action_metadata, config
    )

    reasons = []
    warnings = ["This is a local heuristic proxy and does NOT represent real borrow availability."]

    if liquidity_profile:
        if liquidity_profile.avg_dollar_volume and liquidity_profile.avg_dollar_volume < 1_000_000:
            reasons.append(ExecutionGuardReason.LOW_DOLLAR_VOLUME)
        if liquidity_profile.last_price and liquidity_profile.last_price < 5.0:
            reasons.append(ExecutionGuardReason.LOW_PRICE)
        if liquidity_profile.atr_pct and liquidity_profile.atr_pct > 10.0:
            reasons.append(ExecutionGuardReason.HIGH_VOLATILITY)

    if lifecycle_metadata:
        status_val = lifecycle_metadata.get("status")
        if status_val in ["DELISTED", "SUSPENDED", "REVIEW_REQUIRED"]:
            reasons.append(ExecutionGuardReason.DELISTING_OR_LIFECYCLE_RISK)
            warnings.append("Lifecycle risk detected. Borrow might be restricted.")

    if corporate_action_metadata:
        if corporate_action_metadata.get("recent_split", False) or corporate_action_metadata.get("recent_merger", False):
            reasons.append(ExecutionGuardReason.CORPORATE_ACTION_RISK)
            warnings.append("Corporate action risk detected. Hard to borrow likely.")

    status = classify_borrowability_proxy(score, reasons)

    risk_level = ExecutionRiskLevel.UNKNOWN
    if status == BorrowabilityProxyStatus.LIKELY_UNAVAILABLE or status == BorrowabilityProxyStatus.REVIEW_REQUIRED:
        risk_level = ExecutionRiskLevel.CRITICAL
    elif status == BorrowabilityProxyStatus.LIKELY_HARD:
        risk_level = ExecutionRiskLevel.HIGH
    elif status == BorrowabilityProxyStatus.LIKELY_NORMAL:
        risk_level = ExecutionRiskLevel.MODERATE
    elif status == BorrowabilityProxyStatus.LIKELY_EASY:
        risk_level = ExecutionRiskLevel.LOW

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    return BorrowabilityProxyResult(
        result_id=create_borrowability_proxy_id(symbol),
        symbol=symbol,
        created_at_utc=now_utc,
        status=status,
        risk_level=risk_level,
        score=score,
        reasons=reasons,
        warnings=warnings,
        errors=[],
        metadata={}
    )

def borrowability_proxy_to_text(result: BorrowabilityProxyResult) -> str:
    lines = [
        f"Borrowability Proxy for {result.symbol}:",
        f"  Status: {result.status.value}",
        f"  Risk Level: {result.risk_level.value}",
        f"  Score: {result.score}" if result.score is not None else "  Score: Unknown"
    ]
    if result.reasons:
        lines.append("  Reasons:")
        for r in result.reasons:
            lines.append(f"   - {r.value}")
    if result.warnings:
        lines.append("  Warnings:")
        for w in result.warnings:
            lines.append(f"   - {w}")
    lines.append("  Note: DO NOT rely on this for live trading. No real locate data is used.")
    return "\n".join(lines)
