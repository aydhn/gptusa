"""Offline training loop: panel features -> purged/embargoed CV -> out-of-fold rank IC vs baseline."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from usa_signal_bot.ml_loop.cv import PurgedKFold, assert_no_leakage
from usa_signal_bot.ml_loop.leakage import LeakageReport, check_leakage
from usa_signal_bot.ml_loop.models import MeanBaseline, RidgeModel


@dataclass
class TrainingResult:
    params: Dict[str, float]
    metrics: Dict[str, float]
    fold_ics: List[float]
    baseline_fold_ics: List[float]
    leakage: LeakageReport
    fingerprint: str
    notes: List[str] = field(default_factory=list)


def build_panel(prices: pd.DataFrame, members: pd.DataFrame, horizon: int) -> Tuple[pd.DataFrame, pd.Series]:
    """Features use data <= t. Label = forward ``horizon``-day return, cross-sectionally demeaned."""
    ret1 = prices.pct_change(fill_method=None)
    feats = {
        "mom_21": prices / prices.shift(21) - 1.0,
        "mom_63": prices / prices.shift(63) - 1.0,
        "rev_5": -(prices / prices.shift(5) - 1.0),
        "vol_21": ret1.rolling(21, min_periods=21).std(),
    }
    fwd = prices.shift(-horizon) / prices - 1.0
    fwd = fwd.sub(fwd.where(members).mean(axis=1), axis=0)
    stacked = pd.concat({k: v.where(members).stack() for k, v in feats.items()}, axis=1)
    label = fwd.where(members).stack().rename("label")
    frame = stacked.join(label, how="inner").dropna()
    frame.index.names = ["date", "symbol"]
    return frame.drop(columns="label"), frame["label"]


def _rank_ic(pred: np.ndarray, y: np.ndarray, dates: np.ndarray) -> float:
    df = pd.DataFrame({"p": pred, "y": y, "d": dates})
    ics = []
    for _, g in df.groupby("d"):
        if len(g) >= 5 and g["p"].nunique() > 1:
            ics.append(g["p"].rank().corr(g["y"].rank()))
    return float(np.nanmean(ics)) if ics else 0.0


def _fingerprint(x: pd.DataFrame, y: pd.Series) -> str:
    h = hashlib.sha256()
    h.update(np.round(x.to_numpy(dtype=float), 10).tobytes())
    h.update(np.round(y.to_numpy(dtype=float), 10).tobytes())
    h.update(str(list(x.columns)).encode())
    return h.hexdigest()[:16]


def run_training(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    ridge_alpha: float = 10.0,
    n_splits: int = 5,
    horizon: int = 5,
    embargo: int = 5,
) -> TrainingResult:
    x, y = build_panel(prices, members, horizon)
    dates = x.index.get_level_values("date")
    unique_dates = pd.DatetimeIndex(sorted(dates.unique()))
    date_pos = pd.Series(np.arange(len(unique_dates)), index=unique_dates)
    pos = date_pos.loc[dates].to_numpy()

    # leakage guards: static (per-symbol frames) and structural (every fold)
    leak = LeakageReport()
    for sym in list(x.index.get_level_values("symbol").unique())[:5]:
        fx = x.xs(sym, level="symbol")
        fy = y.xs(sym, level="symbol")
        rep = check_leakage(fx, fy, horizon)
        leak.issues += [f"{sym}: {i}" for i in rep.issues]

    cv = PurgedKFold(n_splits=n_splits, horizon=horizon, embargo=embargo)
    ics: List[float] = []
    base_ics: List[float] = []
    xv, yv = x.to_numpy(dtype=float), y.to_numpy(dtype=float)
    for train_d, test_d in cv.split(len(unique_dates)):
        assert_no_leakage(train_d, test_d, horizon, embargo)
        tr = np.isin(pos, train_d)
        te = np.isin(pos, test_d)
        if tr.sum() < 50 or te.sum() < 10:
            continue
        model = RidgeModel(ridge_alpha).fit(xv[tr], yv[tr])
        base = MeanBaseline().fit(xv[tr], yv[tr])
        ics.append(_rank_ic(model.predict(xv[te]), yv[te], pos[te]))
        base_ics.append(_rank_ic(base.predict(xv[te]), yv[te], pos[te]))
    metrics = {
        "oos_ic_mean": float(np.mean(ics)) if ics else 0.0,
        "baseline_ic_mean": float(np.mean(base_ics)) if base_ics else 0.0,
        "positive_fold_fraction": float(np.mean([i > 0 for i in ics])) if ics else 0.0,
        "n_folds": float(len(ics)),
        "n_rows": float(len(x)),
    }
    return TrainingResult(
        {"ridge_alpha": ridge_alpha, "n_splits": n_splits, "horizon": horizon, "embargo": embargo},
        metrics, ics, base_ics, leak, _fingerprint(x, y),
    )
