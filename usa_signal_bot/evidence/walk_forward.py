"""Cost-aware walk-forward backtest with in-sample parameter selection and out-of-sample stitching.

Leakage rules: weights at t use data <= t; they are held over t+1 (``shift(1)``); parameters for a
test window are chosen only from net returns inside the preceding train window.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple

import pandas as pd

from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.metrics import summarize

WeightFn = Callable[..., pd.DataFrame]


@dataclass(frozen=True)
class WalkForwardConfig:
    train_days: int = 504
    test_days: int = 126
    step_days: int = 126
    purge_days: int = 5  # gap between train end and test start


@dataclass
class FoldResult:
    train_start: pd.Timestamp
    train_end: pd.Timestamp
    test_start: pd.Timestamp
    test_end: pd.Timestamp
    best_params: Dict[str, int]
    train_sharpe: float
    test_sharpe: float


@dataclass
class WalkForwardResult:
    oos_returns: pd.Series
    benchmark_returns: pd.Series
    folds: List[FoldResult] = field(default_factory=list)
    avg_turnover: float = 0.0
    # net returns of EVERY parameter candidate over the stitched OOS dates (inputs for DSR/PBO; n_trials = columns)
    trial_returns: pd.DataFrame = field(default_factory=pd.DataFrame)


def backtest_weights(
    weights: pd.DataFrame, returns: pd.DataFrame, cost: CostModel
) -> Tuple[pd.Series, pd.Series]:
    """Net daily returns and turnover for decision weights ``weights`` (decided at close t, held t+1)."""
    held = weights.shift(1).fillna(0.0)
    gross = (held * returns.fillna(0.0)).sum(axis=1)
    turnover = (held - held.shift(1).fillna(0.0)).abs().sum(axis=1)
    net = gross - cost.cost_series(turnover)
    return net, turnover


def _folds(index: pd.DatetimeIndex, cfg: WalkForwardConfig) -> List[Tuple[int, int, int, int]]:
    out = []
    n = len(index)
    start = 0
    while True:
        tr_end = start + cfg.train_days
        te_start = tr_end + cfg.purge_days
        te_end = te_start + cfg.test_days
        if te_end > n:
            break
        out.append((start, tr_end, te_start, te_end))
        start += cfg.step_days
    return out


def run_walk_forward(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    weight_fn: WeightFn,
    param_grid: List[Dict[str, int]],
    cost: CostModel,
    cfg: WalkForwardConfig,
    benchmark_weights: pd.DataFrame,
) -> WalkForwardResult:
    returns = prices.pct_change(fill_method=None)
    candidates: List[Tuple[Dict[str, int], pd.Series, pd.Series]] = []
    for params in param_grid:
        w = weight_fn(prices, members, **params)
        net, turn = backtest_weights(w, returns, cost)
        candidates.append((params, net, turn))
    bench_net, _ = backtest_weights(benchmark_weights, returns, cost)

    index = prices.index
    oos_parts: List[pd.Series] = []
    bench_parts: List[pd.Series] = []
    turn_parts: List[pd.Series] = []
    folds: List[FoldResult] = []
    for tr_s, tr_e, te_s, te_e in _folds(index, cfg):
        best = None
        for params, net, _turn in candidates:
            sh = summarize(net.iloc[tr_s:tr_e]).sharpe
            if best is None or sh > best[0]:
                best = (sh, params)
        assert best is not None
        params = best[1]
        net, turn = next((n, t) for p, n, t in candidates if p == params)
        oos = net.iloc[te_s:te_e]
        oos_parts.append(oos)
        bench_parts.append(bench_net.iloc[te_s:te_e])
        turn_parts.append(turn.iloc[te_s:te_e])
        folds.append(
            FoldResult(
                index[tr_s], index[tr_e - 1], index[te_s], index[te_e - 1],
                dict(params), best[0], summarize(oos).sharpe,
            )
        )
    if not oos_parts:
        empty = pd.Series(dtype=float)
        return WalkForwardResult(empty, empty, [], 0.0)
    oos_all = pd.concat(oos_parts)
    bench_all = pd.concat(bench_parts)
    turn_all = pd.concat(turn_parts)
    trials = pd.concat([net.rename(str(i)) for i, (_p, net, _t) in enumerate(candidates)], axis=1).loc[oos_all.index]
    return WalkForwardResult(oos_all, bench_all, folds, float(turn_all.mean() * 252), trials)
