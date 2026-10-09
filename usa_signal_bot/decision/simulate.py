"""Day-by-day local paper simulation driven by the decision pipeline (decide at t, fill at t+1 close)."""

from __future__ import annotations

from typing import List, Optional

import pandas as pd

from usa_signal_bot.decision.ledger import PaperLedger
from usa_signal_bot.decision.pipeline import Decision, DecisionConfig, decide
from usa_signal_bot.decision.regime import classify_regime


def simulate_paper(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    cfg: DecisionConfig,
    ledger: PaperLedger,
    momentum_lookback: int = 126,
    skip: int = 21,
    vol_window: int = 20,
) -> List[Decision]:
    """Signals/regime/vol at close t use data <= t; the resulting decision is filled at the t+1 close."""
    benchmark = prices.where(members).mean(axis=1)
    regimes = classify_regime(benchmark)
    score = prices.shift(skip) / prices.shift(momentum_lookback) - 1.0
    score = score.where(members & prices.notna())
    vol = prices.pct_change(fill_method=None).rolling(vol_window, min_periods=vol_window).std()
    decisions: List[Decision] = []
    pending: Optional[Decision] = None
    dates = list(prices.index)
    for i, d in enumerate(dates):
        px = prices.iloc[i]
        day = d.strftime("%Y-%m-%d")
        ledger.accrue_interest(day)
        ledger.close_missing(px, day)
        if pending is not None:
            ledger.rebalance_to(pending.target_weights, px, day, i, pending.exits)
            for sym, why in pending.exits.items():
                if sym in ledger.positions and not pd.isna(px[sym]):
                    ledger._sell(sym, ledger.positions[sym].quantity, float(px[sym]), day, why)
            pending = None
        ledger.mark(px, day)
        ledger.check_invariants()
        if i + 1 >= len(dates):
            break
        signals = {s: float(v) for s, v in score.iloc[i].dropna().items()}
        vols = {s: float(v) for s, v in vol.iloc[i].dropna().items()}
        pending = decide(
            cfg, signals, vols, str(regimes.iloc[i]), ledger.positions, px.to_dict(),
            ledger.current_weights(px), ledger.drawdown(px), i,
        )
        decisions.append(pending)
    return decisions
