import datetime
from typing import Any, Optional, List, Tuple

from usa_signal_bot.core.enums import (
    TradabilityStatus,
    ExecutionRiskLevel,
    ExecutionGuardReason,
    LiquidityStatus,
    ExecutionRealismStatus
)
from usa_signal_bot.execution.liquidity_models import (
    TradabilityGuardResult,
    LiquidityProfile,
    SpreadProxyEstimate,
    SlippageProxyEstimate,
    create_tradability_guard_id
)
from usa_signal_bot.core.config_schema import (
    LiquidityGuardConfig,
    SpreadSlippageProxyConfig,
    VolumeParticipationConfig
)
from usa_signal_bot.execution.liquidity_metrics import calculate_liquidity_profile
from usa_signal_bot.execution.spread_proxy import estimate_spread_proxy
from usa_signal_bot.execution.slippage_proxy import estimate_slippage_proxy
from usa_signal_bot.execution.short_realism_guard import evaluate_short_realism


class TradabilityGuard:
    def __init__(
        self,
        liquidity_config: LiquidityGuardConfig | None = None,
        spread_config: SpreadSlippageProxyConfig | None = None,
        volume_config: VolumeParticipationConfig | None = None
    ):
        self.liquidity_config = liquidity_config or LiquidityGuardConfig()
        self.spread_config = spread_config or SpreadSlippageProxyConfig()
        self.volume_config = volume_config or VolumeParticipationConfig()

    def decide_status(
        self,
        profile: LiquidityProfile | None,
        spread: SpreadProxyEstimate | None,
        slippage: SlippageProxyEstimate | None,
        reasons: list[ExecutionGuardReason]
    ) -> Tuple[TradabilityStatus, ExecutionRiskLevel]:

        status = TradabilityStatus.TRADABLE
        risk = ExecutionRiskLevel.LOW

        if ExecutionGuardReason.STALE_DATA in reasons or \
           ExecutionGuardReason.LOW_PRICE in reasons or \
           ExecutionGuardReason.LOW_VOLUME in reasons or \
           ExecutionGuardReason.LOW_DOLLAR_VOLUME in reasons:
            status = TradabilityStatus.BLOCK_SIGNAL
            risk = ExecutionRiskLevel.CRITICAL
            return status, risk

        if ExecutionGuardReason.HIGH_PARTICIPATION_RATE in reasons:
            if slippage and slippage.participation_rate_pct and slippage.participation_rate_pct > self.volume_config.critical_participation_pct:
                status = TradabilityStatus.BLOCK_BACKTEST_FILL
                risk = ExecutionRiskLevel.CRITICAL
                return status, risk

        if ExecutionGuardReason.HIGH_SLIPPAGE_PROXY in reasons or \
           ExecutionGuardReason.HIGH_SPREAD_PROXY in reasons:
            status = TradabilityStatus.REVIEW_REQUIRED
            risk = ExecutionRiskLevel.HIGH
            return status, risk

        if profile and profile.status == LiquidityStatus.THIN:
            status = TradabilityStatus.CAUTION
            risk = ExecutionRiskLevel.MODERATE

        return status, risk

    def get_recommended_guards(self, status: TradabilityStatus, reasons: list[ExecutionGuardReason]) -> list[str]:
        guards = []
        if status == TradabilityStatus.BLOCK_SIGNAL:
            guards.append("skip_signal_due_to_liquidity")
        elif status == TradabilityStatus.BLOCK_BACKTEST_FILL:
            guards.append("block_backtest_fill_if_participation_too_high")
        elif status == TradabilityStatus.REVIEW_REQUIRED:
            guards.append("require_manual_review")
            guards.append("lower_signal_confidence")
            guards.append("use_conservative_slippage")
        elif status == TradabilityStatus.CAUTION:
            guards.append("reduce_notional")
            guards.append("use_conservative_slippage")

        return guards

    def evaluate_symbol_rows(
        self,
        symbol: str,
        rows: list[dict[str, Any]],
        side: str = "long",
        notional_usd: float | None = None,
        metadata: dict[str, Any] | None = None
    ) -> TradabilityGuardResult:

        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if notional_usd is None:
            notional_usd = self.volume_config.default_notional_usd

        profile = calculate_liquidity_profile(symbol, rows, self.liquidity_config.lookback_bars, self.liquidity_config)
        spread = estimate_spread_proxy(symbol, rows, profile, self.spread_config)
        slippage = estimate_slippage_proxy(symbol, rows, side, notional_usd, profile, self.spread_config)

        reasons = []

        if profile.status == LiquidityStatus.ILLIQUID:
            reasons.append(ExecutionGuardReason.LOW_VOLUME)
            reasons.append(ExecutionGuardReason.LOW_DOLLAR_VOLUME)

        if profile.stale_data_days and profile.stale_data_days > self.liquidity_config.max_stale_days:
            reasons.append(ExecutionGuardReason.STALE_DATA)

        if profile.last_price and profile.last_price < self.liquidity_config.min_price:
            reasons.append(ExecutionGuardReason.LOW_PRICE)

        if spread.status == ExecutionRealismStatus.UNREALISTIC:
            reasons.append(ExecutionGuardReason.HIGH_SPREAD_PROXY)

        if slippage.status == ExecutionRealismStatus.UNREALISTIC:
            reasons.append(ExecutionGuardReason.HIGH_SLIPPAGE_PROXY)

        if slippage.participation_rate_pct and slippage.participation_rate_pct > self.volume_config.max_participation_pct:
            reasons.append(ExecutionGuardReason.HIGH_PARTICIPATION_RATE)

        if profile.gap_pct and profile.gap_pct > 10.0:
            reasons.append(ExecutionGuardReason.LARGE_GAP)

        # If short, delegate to short realism guard
        if side.lower() == "short":
            short_res = evaluate_short_realism(
                symbol, rows, notional_usd,
                lifecycle_metadata=metadata.get("lifecycle") if metadata else None,
                corporate_action_metadata=metadata.get("corporate_actions") if metadata else None,
                liquidity_profile=profile
            )
            reasons.extend(short_res.reasons)

        # Deduplicate
        reasons = list(set(reasons))

        status, risk = self.decide_status(profile, spread, slippage, reasons)
        guards = self.get_recommended_guards(status, reasons)

        # Merge warnings
        warnings = []
        warnings.extend(profile.warnings)
        warnings.extend(spread.warnings)
        warnings.extend(slippage.warnings)
        if side.lower() == "short":
             warnings.append("Short side execution may be blocked by borrow proxy limitations.")

        # Add limitation notice
        warnings.append("Not investment advice. Guard uses heuristics. No live orders are simulated.")

        return TradabilityGuardResult(
            guard_id=create_tradability_guard_id(symbol),
            symbol=symbol,
            created_at_utc=now_utc,
            status=status,
            risk_level=risk,
            liquidity_profile=profile,
            spread_estimate=spread,
            slippage_estimate=slippage,
            reasons=reasons,
            recommended_guards=guards,
            warnings=list(set(warnings)),
            errors=[],
            metadata={}
        )

    def evaluate_many(
        self,
        payload: dict[str, list[dict[str, Any]]],
        side: str = "long",
        notional_usd: float | None = None
    ) -> list[TradabilityGuardResult]:
        results = []
        for symbol, rows in payload.items():
            results.append(self.evaluate_symbol_rows(symbol, rows, side, notional_usd))
        return results
