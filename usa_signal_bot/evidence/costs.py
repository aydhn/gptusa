"""Transaction cost model: proportional commission plus slippage per unit of turnover."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CostModel:
    commission_bps: float = 1.0
    slippage_bps: float = 5.0

    @property
    def round_trip_bps_per_unit(self) -> float:
        return self.commission_bps + self.slippage_bps

    def cost_series(self, turnover: pd.Series) -> pd.Series:
        """Return cost as a fraction of equity for each period (turnover = sum |weight change|)."""
        return turnover.abs() * (self.commission_bps + self.slippage_bps) / 10_000.0
