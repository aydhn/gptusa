"""Cost / capacity sensitivity of the local simulated paper pipeline (no orders; ledger is in-memory only).

Capacity uses a square-root impact assumption: extra_bps = impact_coef_bps * sqrt(position_dollars / adv_dollars).
``adv_dollars`` is an ASSUMED per-symbol average daily dollar volume (no volume feed here), so results are
illustrative sensitivities, not capacity estimates.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Sequence

import pandas as pd

from usa_signal_bot.decision.ledger import PaperLedger
from usa_signal_bot.decision.pipeline import DecisionConfig
from usa_signal_bot.decision.simulate import simulate_paper
from usa_signal_bot.evidence.costs import CostModel


@dataclass(frozen=True)
class SensitivityPoint:
    capital: float
    slippage_bps: float
    effective_slippage_bps: float
    final_equity: float
    total_return: float
    n_fills: int


def impact_bps(position_dollars: float, adv_dollars: float, coef_bps: float = 10.0) -> float:
    if adv_dollars <= 0:
        raise ValueError("adv_dollars must be > 0")
    return coef_bps * math.sqrt(max(position_dollars, 0.0) / adv_dollars)


def cost_capacity_grid(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    cfg: DecisionConfig,
    capitals: Sequence[float] = (1e5, 1e6, 1e7),
    slippage_bps: Sequence[float] = (2.0, 5.0, 10.0, 20.0),
    adv_dollars: float = 5e7,
    commission_bps: float = 1.0,
    impact_coef_bps: float = 10.0,
) -> List[SensitivityPoint]:
    out: List[SensitivityPoint] = []
    max_w = cfg.limits.max_weight
    for cap in capitals:
        extra = impact_bps(cap * max_w, adv_dollars, impact_coef_bps)
        for slip in slippage_bps:
            eff = slip + extra
            led = PaperLedger(initial_cash=cap, cost=CostModel(commission_bps, eff))
            simulate_paper(prices, members, cfg, led)
            final = list(led.equity_curve.values())[-1] if led.equity_curve else cap
            out.append(SensitivityPoint(cap, slip, eff, final, final / cap - 1.0, len(led.fills)))
    return out
