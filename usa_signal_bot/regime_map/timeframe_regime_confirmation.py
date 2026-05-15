from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    RegimeTimeframe,
    RegimeConfirmationStatus,
    TrendRegime,
    VolatilityMapRegime,
    MomentumRegime,
    LiquidityMapRegime
)
from usa_signal_bot.regime_map.regime_map_models import (
    TimeframeRegimeSnapshot,
    MultiTimeframeRegimeConfirmation,
    create_timeframe_regime_snapshot_id,
    create_multi_timeframe_confirmation_id
)
from usa_signal_bot.regime_map.timeframe_resampler import resample_ohlcv_rows
from usa_signal_bot.regime_map.trend_confirmation import classify_trend_regime, trend_regime_confidence
from usa_signal_bot.regime_map.volatility_confirmation import classify_volatility_map_regime, volatility_regime_confidence
from usa_signal_bot.regime_map.momentum_confirmation import classify_momentum_regime, momentum_regime_confidence
from usa_signal_bot.regime_map.liquidity_confirmation import classify_liquidity_map_regime, liquidity_regime_confidence

class MultiTimeframeRegimeConfirmationEngine:
    def __init__(self, timeframes: list[RegimeTimeframe] | None = None):
        self.timeframes = timeframes or [RegimeTimeframe.DAILY, RegimeTimeframe.WEEKLY, RegimeTimeframe.MONTHLY]

    def build_timeframe_snapshot(self, symbol: str, rows: list[dict[str, Any]], timeframe: RegimeTimeframe) -> TimeframeRegimeSnapshot:
        resampled = resample_ohlcv_rows(rows, timeframe)

        trend, trend_ev = classify_trend_regime(resampled)
        vol, vol_ev = classify_volatility_map_regime(resampled)
        mom, mom_ev = classify_momentum_regime(resampled)
        liq, liq_ev = classify_liquidity_map_regime(resampled)

        # Combine evidence
        evidence = {
            "trend": trend_ev,
            "volatility": vol_ev,
            "momentum": mom_ev,
            "liquidity": liq_ev,
            "row_count": len(resampled)
        }

        # Rough confidence
        confidences = [
            trend_regime_confidence(trend, trend_ev),
            volatility_regime_confidence(vol, vol_ev),
            momentum_regime_confidence(mom, mom_ev),
            liquidity_regime_confidence(liq, liq_ev)
        ]
        valid_confidences = [c for c in confidences if c is not None]
        confidence = sum(valid_confidences) / len(valid_confidences) if valid_confidences else None

        return TimeframeRegimeSnapshot(
            snapshot_id=create_timeframe_regime_snapshot_id(symbol, timeframe),
            symbol=symbol,
            timeframe=timeframe,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            trend_regime=trend,
            volatility_regime=vol,
            momentum_regime=mom,
            liquidity_regime=liq,
            confidence=confidence,
            evidence=evidence,
            warnings=[],
            errors=[]
        )

    def determine_confirmation_status(self, snapshots: list[TimeframeRegimeSnapshot]) -> RegimeConfirmationStatus:
        if not snapshots:
            return RegimeConfirmationStatus.INSUFFICIENT_DATA

        trend_dirs = set()
        for s in snapshots:
            if s.trend_regime in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]:
                trend_dirs.add(1)
            elif s.trend_regime in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
                trend_dirs.add(-1)
            elif s.trend_regime != TrendRegime.INSUFFICIENT_DATA:
                trend_dirs.add(0)

        if not trend_dirs or len(trend_dirs) == 0:
            return RegimeConfirmationStatus.INSUFFICIENT_DATA

        if len(trend_dirs) == 1 and 0 not in trend_dirs:
            # All same direction
            if len(snapshots) >= 2: # At least Daily + Weekly
                return RegimeConfirmationStatus.CONFIRMED
            return RegimeConfirmationStatus.PARTIAL

        if 1 in trend_dirs and -1 in trend_dirs:
             return RegimeConfirmationStatus.CONFLICTED

        if 0 in trend_dirs and (1 in trend_dirs or -1 in trend_dirs):
            return RegimeConfirmationStatus.DIVERGENT

        return RegimeConfirmationStatus.UNKNOWN

    def dominant_trend(self, snapshots: list[TimeframeRegimeSnapshot]) -> TrendRegime:
        if not snapshots: return TrendRegime.UNKNOWN
        # Simplest approach: use daily as dominant if available, else first
        for s in snapshots:
             if s.timeframe == RegimeTimeframe.DAILY:
                 return s.trend_regime
        return snapshots[0].trend_regime

    def dominant_volatility(self, snapshots: list[TimeframeRegimeSnapshot]) -> VolatilityMapRegime:
        if not snapshots: return VolatilityMapRegime.UNKNOWN
        for s in snapshots:
             if s.timeframe == RegimeTimeframe.DAILY:
                 return s.volatility_regime
        return snapshots[0].volatility_regime

    def dominant_momentum(self, snapshots: list[TimeframeRegimeSnapshot]) -> MomentumRegime:
         if not snapshots: return MomentumRegime.UNKNOWN
         for s in snapshots:
             if s.timeframe == RegimeTimeframe.DAILY:
                 return s.momentum_regime
         return snapshots[0].momentum_regime

    def dominant_liquidity(self, snapshots: list[TimeframeRegimeSnapshot]) -> LiquidityMapRegime:
        if not snapshots: return LiquidityMapRegime.UNKNOWN
        for s in snapshots:
             if s.timeframe == RegimeTimeframe.DAILY:
                 return s.liquidity_regime
        return snapshots[0].liquidity_regime

    def confirm_symbol(self, symbol: str, rows: list[dict[str, Any]]) -> MultiTimeframeRegimeConfirmation:
        snapshots = []
        warnings = []

        for tf in self.timeframes:
            snap = self.build_timeframe_snapshot(symbol, rows, tf)
            snapshots.append(snap)
            if snap.trend_regime == TrendRegime.INSUFFICIENT_DATA:
                warnings.append(f"Insufficient data for {tf.value}")

        status = self.determine_confirmation_status(snapshots)

        confidences = [s.confidence for s in snapshots if s.confidence is not None]
        confidence = sum(confidences) / len(confidences) if confidences else None

        conflicts = []
        if status in [RegimeConfirmationStatus.CONFLICTED, RegimeConfirmationStatus.DIVERGENT]:
             conflicts.append("Timeframe trend divergence detected.")

        return MultiTimeframeRegimeConfirmation(
            confirmation_id=create_multi_timeframe_confirmation_id(symbol),
            symbol=symbol,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            snapshots=snapshots,
            status=status,
            dominant_trend_regime=self.dominant_trend(snapshots),
            dominant_volatility_regime=self.dominant_volatility(snapshots),
            dominant_momentum_regime=self.dominant_momentum(snapshots),
            dominant_liquidity_regime=self.dominant_liquidity(snapshots),
            confidence=confidence,
            conflicts=conflicts,
            warnings=warnings,
            errors=[]
        )

    def confirm_many(self, symbol_rows: dict[str, list[dict[str, Any]]]) -> list[MultiTimeframeRegimeConfirmation]:
        return [self.confirm_symbol(symbol, rows) for symbol, rows in symbol_rows.items()]
