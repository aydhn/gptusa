import datetime
from typing import Any
from usa_signal_bot.core.enums import CrossSectionalRegime, TrendRegime, VolatilityMapRegime, MomentumRegime, LiquidityMapRegime, BreadthRegime
from usa_signal_bot.regime_map.regime_map_models import CrossSectionalRegimeMap, MultiTimeframeRegimeConfirmation, create_cross_sectional_regime_map_id
from usa_signal_bot.regime_map.breadth_proxy import calculate_breadth_score, classify_breadth_regime
from usa_signal_bot.regime_map.dispersion_proxy import dispersion_score

class CrossSectionalRegimeMapBuilder:
    def __init__(self, universe_name: str = "usa_default"):
        self.universe_name = universe_name

    def build_map(self, confirmations: list[MultiTimeframeRegimeConfirmation], symbol_rows: dict | None = None) -> CrossSectionalRegimeMap:
        counts = self.summarize_counts(confirmations)
        breadth = classify_breadth_regime(confirmations)
        dispersion = dispersion_score(confirmations, symbol_rows)
        breadth_val = calculate_breadth_score(confirmations)

        regime = self.classify_cross_sectional_regime(confirmations, breadth, dispersion)

        warnings = []
        if len(confirmations) < 20:
             warnings.append("Small universe, cross-sectional regime may be unreliable.")

        if dispersion and dispersion > 60:
             warnings.append("High dispersion indicates rotation or stock-picker's market.")

        return CrossSectionalRegimeMap(
            map_id=create_cross_sectional_regime_map_id(self.universe_name),
            universe_name=self.universe_name,
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            symbol_count=len(confirmations),
            cross_sectional_regime=regime,
            breadth_regime=breadth,
            uptrend_count=counts["uptrend"],
            downtrend_count=counts["downtrend"],
            range_count=counts["range"],
            high_vol_count=counts["high_vol"],
            thin_liquidity_count=counts["thin_liquidity"],
            momentum_positive_count=counts["momentum_positive"],
            momentum_negative_count=counts["momentum_negative"],
            dispersion_score=dispersion,
            breadth_score=breadth_val,
            symbol_snapshots=confirmations,
            warnings=warnings,
            errors=[],
            metadata=self.build_symbol_metadata(confirmations)
        )

    def classify_cross_sectional_regime(self, confirmations: list[MultiTimeframeRegimeConfirmation], breadth: BreadthRegime, dispersion: float | None) -> CrossSectionalRegime:
        if not confirmations or len(confirmations) < 5:
            return CrossSectionalRegime.INSUFFICIENT_DATA

        counts = self.summarize_counts(confirmations)
        total = len(confirmations)
        up_ratio = counts["uptrend"] / total
        down_ratio = counts["downtrend"] / total

        if up_ratio > 0.60 and breadth in [BreadthRegime.BROAD_RISK_ON, BreadthRegime.RISK_ON]:
            if dispersion and dispersion > 50:
                 return CrossSectionalRegime.SELECTIVE_UPTREND
            return CrossSectionalRegime.BROAD_UPTREND

        if down_ratio > 0.60 and breadth in [BreadthRegime.RISK_OFF, BreadthRegime.DETERIORATING]:
             return CrossSectionalRegime.BROAD_DOWNTREND

        if up_ratio > 0.40 and dispersion and dispersion > 40:
             return CrossSectionalRegime.ROTATION

        if breadth == BreadthRegime.RISK_OFF:
             return CrossSectionalRegime.RISK_OFF

        if dispersion and dispersion > 60:
             return CrossSectionalRegime.DISPERSION_HIGH

        return CrossSectionalRegime.MIXED

    def summarize_counts(self, confirmations: list[MultiTimeframeRegimeConfirmation]) -> dict[str, int]:
        counts = {
            "uptrend": 0, "downtrend": 0, "range": 0,
            "high_vol": 0, "thin_liquidity": 0,
            "momentum_positive": 0, "momentum_negative": 0
        }
        for c in confirmations:
            if c.dominant_trend_regime in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]:
                counts["uptrend"] += 1
            elif c.dominant_trend_regime in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
                counts["downtrend"] += 1
            elif c.dominant_trend_regime in [TrendRegime.RANGE, TrendRegime.CHOPPY]:
                counts["range"] += 1

            if c.dominant_volatility_regime in [VolatilityMapRegime.HIGH, VolatilityMapRegime.EXTREME]:
                counts["high_vol"] += 1

            if c.dominant_liquidity_regime in [LiquidityMapRegime.THIN, LiquidityMapRegime.ILLIQUID]:
                counts["thin_liquidity"] += 1

            if c.dominant_momentum_regime in [MomentumRegime.POSITIVE, MomentumRegime.STRONG_POSITIVE]:
                counts["momentum_positive"] += 1
            elif c.dominant_momentum_regime in [MomentumRegime.NEGATIVE, MomentumRegime.STRONG_NEGATIVE]:
                counts["momentum_negative"] += 1

        return counts

    def build_symbol_metadata(self, confirmations: list[MultiTimeframeRegimeConfirmation]) -> dict[str, Any]:
        return {}
