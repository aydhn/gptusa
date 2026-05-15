from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    CrossSectionalRegime,
    BreadthRegime,
    TrendRegime,
    VolatilityMapRegime,
    MomentumRegime,
    LiquidityMapRegime
)
from usa_signal_bot.regime_map.regime_map_models import (
    MultiTimeframeRegimeConfirmation,
    CrossSectionalRegimeMap,
    create_cross_sectional_regime_map_id
)
from usa_signal_bot.regime_map.breadth_proxy import classify_breadth_regime, calculate_breadth_score
from usa_signal_bot.regime_map.dispersion_proxy import dispersion_score


class CrossSectionalRegimeMapBuilder:
    def __init__(self, universe_name: str = "usa_default"):
        self.universe_name = universe_name

    def summarize_counts(self, confirmations: list[MultiTimeframeRegimeConfirmation]) -> dict[str, int]:
        counts = {
            "uptrend_count": 0,
            "downtrend_count": 0,
            "range_count": 0,
            "high_vol_count": 0,
            "thin_liquidity_count": 0,
            "momentum_positive_count": 0,
            "momentum_negative_count": 0
        }

        for c in confirmations:
            if c.dominant_trend_regime in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]:
                counts["uptrend_count"] += 1
            elif c.dominant_trend_regime in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
                counts["downtrend_count"] += 1
            elif c.dominant_trend_regime in [TrendRegime.RANGE, TrendRegime.CHOPPY]:
                counts["range_count"] += 1

            if c.dominant_volatility_regime in [VolatilityMapRegime.HIGH, VolatilityMapRegime.EXTREME, VolatilityMapRegime.EXPANDING]:
                counts["high_vol_count"] += 1

            if c.dominant_liquidity_regime in [LiquidityMapRegime.THIN, LiquidityMapRegime.THINNING, LiquidityMapRegime.ILLIQUID]:
                counts["thin_liquidity_count"] += 1

            if c.dominant_momentum_regime in [MomentumRegime.POSITIVE, MomentumRegime.STRONG_POSITIVE]:
                counts["momentum_positive_count"] += 1
            elif c.dominant_momentum_regime in [MomentumRegime.NEGATIVE, MomentumRegime.STRONG_NEGATIVE]:
                counts["momentum_negative_count"] += 1

        return counts

    def classify_cross_sectional_regime(self, confirmations: list[MultiTimeframeRegimeConfirmation], breadth: BreadthRegime, dispersion: float | None) -> CrossSectionalRegime:
        if len(confirmations) < 10:
            return CrossSectionalRegime.INSUFFICIENT_DATA

        if breadth in [BreadthRegime.BROAD_RISK_ON, BreadthRegime.RISK_ON]:
            if dispersion is not None and dispersion > 60:
                return CrossSectionalRegime.ROTATION # Broad participation but high dispersion = rotation
            return CrossSectionalRegime.BROAD_UPTREND

        counts = self.summarize_counts(confirmations)
        uptrend_ratio = counts["uptrend_count"] / len(confirmations)

        if uptrend_ratio > 0.3 and dispersion is not None and dispersion > 50:
             return CrossSectionalRegime.SELECTIVE_UPTREND

        if breadth == BreadthRegime.RISK_OFF or uptrend_ratio < 0.2:
            return CrossSectionalRegime.BROAD_DOWNTREND

        if dispersion is not None and dispersion > 70:
            return CrossSectionalRegime.DISPERSION_HIGH

        return CrossSectionalRegime.MIXED

    def build_symbol_metadata(self, confirmations: list[MultiTimeframeRegimeConfirmation]) -> dict[str, Any]:
         # Could extract interesting leaders/laggards here for metadata
         return {}

    def build_map(self, confirmations: list[MultiTimeframeRegimeConfirmation], symbol_rows: dict[str, list[dict[str, Any]]] | None = None) -> CrossSectionalRegimeMap:
        counts = self.summarize_counts(confirmations)
        breadth_regime = classify_breadth_regime(confirmations)
        breadth_val = calculate_breadth_score(confirmations)
        disp_score = dispersion_score(confirmations, symbol_rows)

        xs_regime = self.classify_cross_sectional_regime(confirmations, breadth_regime, disp_score)

        warnings = []
        if len(confirmations) < 20:
             warnings.append(f"Small universe size ({len(confirmations)}). Map may be unreliable.")
        if disp_score is not None and disp_score > 80:
             warnings.append("Extremely high dispersion detected.")

        return CrossSectionalRegimeMap(
            map_id=create_cross_sectional_regime_map_id(self.universe_name),
            universe_name=self.universe_name,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            symbol_count=len(confirmations),
            cross_sectional_regime=xs_regime,
            breadth_regime=breadth_regime,
            uptrend_count=counts["uptrend_count"],
            downtrend_count=counts["downtrend_count"],
            range_count=counts["range_count"],
            high_vol_count=counts["high_vol_count"],
            thin_liquidity_count=counts["thin_liquidity_count"],
            momentum_positive_count=counts["momentum_positive_count"],
            momentum_negative_count=counts["momentum_negative_count"],
            dispersion_score=disp_score,
            breadth_score=breadth_val,
            symbol_snapshots=confirmations,
            warnings=warnings,
            errors=[],
            metadata=self.build_symbol_metadata(confirmations)
        )
