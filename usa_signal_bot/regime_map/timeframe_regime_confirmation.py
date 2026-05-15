from typing import Any
import datetime

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

        conf_trend = trend_regime_confidence(trend, trend_ev) or 0
        conf_vol = volatility_regime_confidence(vol, vol_ev) or 0
        conf_mom = momentum_regime_confidence(mom, mom_ev) or 0
        conf_liq = liquidity_regime_confidence(liq, liq_ev) or 0

        confidence = (conf_trend + conf_vol + conf_mom + conf_liq) / 4.0
        if trend == TrendRegime.INSUFFICIENT_DATA:
            confidence = None

        evidence = {
            "trend": trend_ev,
            "volatility": vol_ev,
            "momentum": mom_ev,
            "liquidity": liq_ev
        }

        return TimeframeRegimeSnapshot(
            snapshot_id=create_timeframe_regime_snapshot_id(symbol, timeframe),
            symbol=symbol,
            timeframe=timeframe,
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            trend_regime=trend,
            volatility_regime=vol,
            momentum_regime=mom,
            liquidity_regime=liq,
            confidence=confidence,
            evidence=evidence,
            warnings=[],
            errors=[]
        )

    def confirm_symbol(self, symbol: str, rows: list[dict[str, Any]]) -> MultiTimeframeRegimeConfirmation:
        snapshots = []
        for tf in self.timeframes:
            snapshots.append(self.build_timeframe_snapshot(symbol, rows, tf))

        status = self.determine_confirmation_status(snapshots)
        dom_trend = self.dominant_trend(snapshots)
        dom_vol = self.dominant_volatility(snapshots)
        dom_mom = self.dominant_momentum(snapshots)
        dom_liq = self.dominant_liquidity(snapshots)

        confs = [s.confidence for s in snapshots if s.confidence is not None]
        confidence = sum(confs)/len(confs) if confs else None

        warnings = []
        conflicts = []
        if status in [RegimeConfirmationStatus.CONFLICTED, RegimeConfirmationStatus.DIVERGENT]:
            warnings.append("Timeframe regimes are divergent or conflicted.")
            conflicts.append("Daily trend disagrees with weekly/monthly trend.")

        if dom_vol in [VolatilityMapRegime.HIGH, VolatilityMapRegime.EXTREME] and status == RegimeConfirmationStatus.DIVERGENT:
             warnings.append("High volatility coupled with timeframe divergence.")

        return MultiTimeframeRegimeConfirmation(
            confirmation_id=create_multi_timeframe_confirmation_id(symbol),
            symbol=symbol,
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            snapshots=snapshots,
            status=status,
            dominant_trend_regime=dom_trend,
            dominant_volatility_regime=dom_vol,
            dominant_momentum_regime=dom_mom,
            dominant_liquidity_regime=dom_liq,
            confidence=confidence,
            conflicts=conflicts,
            warnings=warnings,
            errors=[]
        )

    def confirm_many(self, symbol_rows: dict[str, list[dict[str, Any]]]) -> list[MultiTimeframeRegimeConfirmation]:
        results = []
        for sym, rows in symbol_rows.items():
            results.append(self.confirm_symbol(sym, rows))
        return results

    def determine_confirmation_status(self, snapshots: list[TimeframeRegimeSnapshot]) -> RegimeConfirmationStatus:
        if not snapshots:
            return RegimeConfirmationStatus.INSUFFICIENT_DATA

        trends = [s.trend_regime for s in snapshots]
        if any(t == TrendRegime.INSUFFICIENT_DATA for t in trends):
            if len(trends) > 1 and trends[0] != TrendRegime.INSUFFICIENT_DATA:
                 return RegimeConfirmationStatus.PARTIAL
            return RegimeConfirmationStatus.INSUFFICIENT_DATA

        up_trends = [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]
        down_trends = [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]

        all_up = all(t in up_trends for t in trends)
        all_down = all(t in down_trends for t in trends)

        if all_up or all_down:
            return RegimeConfirmationStatus.CONFIRMED

        # Check daily vs weekly
        daily = next((s.trend_regime for s in snapshots if s.timeframe == RegimeTimeframe.DAILY), None)
        weekly = next((s.trend_regime for s in snapshots if s.timeframe == RegimeTimeframe.WEEKLY), None)
        monthly = next((s.trend_regime for s in snapshots if s.timeframe == RegimeTimeframe.MONTHLY), None)

        if daily in up_trends and weekly in down_trends:
             return RegimeConfirmationStatus.CONFLICTED
        if daily in down_trends and weekly in up_trends:
             return RegimeConfirmationStatus.CONFLICTED

        if daily in up_trends and monthly in down_trends:
            return RegimeConfirmationStatus.DIVERGENT

        return RegimeConfirmationStatus.PARTIAL

    def dominant_trend(self, snapshots: list[TimeframeRegimeSnapshot]) -> TrendRegime:
        weekly = next((s.trend_regime for s in snapshots if s.timeframe == RegimeTimeframe.WEEKLY), None)
        daily = next((s.trend_regime for s in snapshots if s.timeframe == RegimeTimeframe.DAILY), None)
        # Default to weekly if available, else daily
        if weekly and weekly != TrendRegime.INSUFFICIENT_DATA:
            return weekly
        if daily:
             return daily
        return TrendRegime.UNKNOWN

    def dominant_volatility(self, snapshots: list[TimeframeRegimeSnapshot]) -> VolatilityMapRegime:
        daily = next((s.volatility_regime for s in snapshots if s.timeframe == RegimeTimeframe.DAILY), None)
        return daily or VolatilityMapRegime.UNKNOWN

    def dominant_momentum(self, snapshots: list[TimeframeRegimeSnapshot]) -> MomentumRegime:
        daily = next((s.momentum_regime for s in snapshots if s.timeframe == RegimeTimeframe.DAILY), None)
        return daily or MomentumRegime.UNKNOWN

    def dominant_liquidity(self, snapshots: list[TimeframeRegimeSnapshot]) -> LiquidityMapRegime:
        daily = next((s.liquidity_regime for s in snapshots if s.timeframe == RegimeTimeframe.DAILY), None)
        return daily or LiquidityMapRegime.UNKNOWN
