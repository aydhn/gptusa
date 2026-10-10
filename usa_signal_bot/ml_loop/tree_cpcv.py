"""Tree-based (scikit-learn) cross-sectional models evaluated with Combinatorial Purged CV backtest PATHS.

Research only. Every model is a CANDIDATE: each CPCV path is turned into long-only weights, run through the same
cost-aware, cash-interest backtest as ``evidence/``, and judged on the distribution of path excess returns versus the
equal-weight benchmark (DSR with the cumulative trial count + Hansen SPA). Optional meta-labeling (Lopez de Prado):
a primary factor-mix signal proposes positions and a tree model vetoes those unlikely to beat the market.
scikit-learn is optional (imported lazily).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.factors import factor_mix_weights
from usa_signal_bot.evidence.metrics import summarize
from usa_signal_bot.evidence.rates import RateLike
from usa_signal_bot.evidence.spa import spa_test
from usa_signal_bot.evidence.stats import deflated_sharpe_ratio
from usa_signal_bot.evidence.strategies import equal_weight_benchmark
from usa_signal_bot.evidence.walk_forward import backtest_weights
from usa_signal_bot.ml_loop.cpcv import CombinatorialPurgedCV, assert_cpcv_no_leakage


def build_features(prices: pd.DataFrame, members: pd.DataFrame, horizon: int) -> Tuple[pd.DataFrame, pd.Series]:
    """Panel (date, symbol) features using data <= t; label = forward ``horizon`` return minus cross-sectional mean."""
    r1 = prices.pct_change(fill_method=None)
    feats = {
        "mom_21": prices / prices.shift(21) - 1.0,
        "mom_63": prices / prices.shift(63) - 1.0,
        "mom_252_21": prices.shift(21) / prices.shift(252) - 1.0,
        "rev_5": -(prices / prices.shift(5) - 1.0),
        "vol_21": r1.rolling(21, min_periods=21).std(),
        "vol_126": r1.rolling(126, min_periods=126).std(),
        "dist_252": prices / prices.rolling(252, min_periods=252).max() - 1.0,
        "stab_126": r1.rolling(126, min_periods=126).mean() / r1.rolling(126, min_periods=126).std().replace(0, np.nan),
    }
    fwd = prices.shift(-horizon) / prices - 1.0
    fwd = fwd.sub(fwd.where(members).mean(axis=1), axis=0)
    x = pd.concat({k: v.where(members).stack() for k, v in feats.items()}, axis=1)
    y = fwd.where(members).stack().rename("label")
    frame = x.join(y, how="inner").dropna()
    frame.index.names = ["date", "symbol"]
    return frame.drop(columns="label"), frame["label"]


def make_model(kind: str, seed: int = 0):
    try:
        from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
    except ImportError as exc:  # optional dependency
        raise RuntimeError("scikit-learn is required for tree models (pip install scikit-learn)") from exc
    if kind == "hgb":
        return HistGradientBoostingClassifier(max_iter=80, max_depth=3, learning_rate=0.05, l2_regularization=1.0, random_state=seed)
    if kind == "rf":
        return RandomForestClassifier(n_estimators=80, max_depth=5, min_samples_leaf=300, n_jobs=-1, random_state=seed)
    raise ValueError(f"unknown model kind '{kind}'")


@dataclass
class CPCVModelResult:
    model_kind: str
    meta_labeling: bool
    n_paths: int
    path_cagr: List[float]
    path_sharpe: List[float]
    path_excess_sharpe: List[float]
    bench_cagr: float
    bench_sharpe: float
    dsr_excess: float
    spa_p: float
    leakage_clean: bool
    n_trials: int
    eligible: bool = False
    reasons: List[str] = field(default_factory=list)
    fingerprint: str = ""

    def metrics(self) -> Dict[str, float]:
        return {
            "median_path_cagr": float(np.median(self.path_cagr)),
            "median_path_sharpe": float(np.median(self.path_sharpe)),
            "median_path_excess_sharpe": float(np.median(self.path_excess_sharpe)),
            "positive_path_fraction": float(np.mean([s > 0 for s in self.path_excess_sharpe])),
            "bench_cagr": self.bench_cagr,
            "dsr_excess": self.dsr_excess,
            "spa_p": self.spa_p,
            "n_paths": float(self.n_paths),
            "n_trials": float(self.n_trials),
        }


def judge(res: CPCVModelResult, min_dsr: float = 0.95, max_spa_p: float = 0.05) -> CPCVModelResult:
    """ELIGIBLE only with clean leakage, median path excess Sharpe > 0, DSR(excess) >= min_dsr and SPA p <= max_spa_p."""
    reasons: List[str] = []
    if not res.leakage_clean:
        reasons.append("leakage check not clean")
    if not np.median(res.path_excess_sharpe) > 0:
        reasons.append("median path excess Sharpe <= 0")
    if not res.dsr_excess >= min_dsr:
        reasons.append(f"dsr_excess {res.dsr_excess:.2f} < {min_dsr}")
    if not res.spa_p <= max_spa_p:
        reasons.append(f"spa_p {res.spa_p:.3f} > {max_spa_p}")
    res.reasons, res.eligible = reasons, not reasons
    return res


def _scores_to_weights(scores: pd.Series, members: pd.DataFrame, prices: pd.DataFrame, top_frac: float) -> pd.DataFrame:
    s = scores.unstack("symbol").reindex(index=prices.index, columns=prices.columns)
    s = s.where(members & prices.notna())
    rank = s.rank(axis=1, ascending=False, pct=True)
    sel = ((rank <= top_frac) & s.notna()).astype(float)
    n = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(n, axis=0).fillna(0.0)


def run_tree_cpcv(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    cost: Optional[CostModel] = None,
    cash_rate: RateLike = 0.0,
    kind: str = "hgb",
    meta_labeling: bool = False,
    n_groups: int = 6,
    n_test_groups: int = 2,
    horizon: int = 5,
    embargo: int = 5,
    top_frac: float = 0.3,
    n_trials: int = 1,
    var_sr_trials: Optional[float] = None,
    seed: int = 0,
) -> CPCVModelResult:
    cost = cost or CostModel()
    x, y = build_features(prices, members, horizon)
    dates = x.index.get_level_values("date")
    uniq = pd.DatetimeIndex(sorted(dates.unique()))
    pos = pd.Series(np.arange(len(uniq)), index=uniq).loc[dates].to_numpy()
    xv, yb = x.to_numpy(dtype=float), (y.to_numpy() > 0).astype(int)

    prim_w = factor_mix_weights(prices, members, 252, 0.4) if meta_labeling else None
    primary_pick = (prim_w.stack().reindex(x.index).fillna(0.0).to_numpy() > 0) if meta_labeling else None

    cv = CombinatorialPurgedCV(n_groups, n_test_groups, horizon, embargo)
    bounds = cv._bounds(len(uniq))
    split_scores: Dict[Tuple[int, int], pd.Series] = {}
    leakage_clean = True
    for si, (train_d, test_d, combo) in enumerate(cv.split(len(uniq))):
        try:
            assert_cpcv_no_leakage(train_d, test_d, horizon, embargo)
        except AssertionError:
            leakage_clean = False
            continue
        tr = np.isin(pos, train_d)
        te = np.isin(pos, test_d)
        if meta_labeling:
            tr = tr & primary_pick
        if tr.sum() < 200 or yb[tr].min() == yb[tr].max():
            continue
        model = make_model(kind, seed).fit(xv[tr], yb[tr])
        proba = pd.Series(model.predict_proba(xv[te])[:, 1], index=x.index[te])
        tpos = pos[te]
        for g in combo:
            m = (tpos >= bounds[g]) & (tpos < bounds[g + 1])
            split_scores[(si, g)] = proba[m]

    returns = prices.pct_change(fill_method=None)
    bench_net, _ = backtest_weights(equal_weight_benchmark(prices, members), returns, cost, cash_rate)
    p_cagr: List[float] = []
    p_sh: List[float] = []
    p_ex: List[float] = []
    ex_cols: List[pd.Series] = []
    valid = bench_net.index[:0]
    for path in cv.paths():
        parts = [split_scores[k] for k in path if k in split_scores]
        if len(parts) != len(path):
            continue
        scores = pd.concat(parts)
        if meta_labeling:
            keep = scores.unstack("symbol").reindex(index=prices.index, columns=prices.columns) > 0.5
            w = prim_w.where(keep, 0.0)
        else:
            w = _scores_to_weights(scores, members, prices, top_frac)
        net, _ = backtest_weights(w, returns, cost, cash_rate)
        d = scores.index.get_level_values("date")
        valid = net.index[(net.index >= d.min()) & (net.index <= d.max())]
        s = summarize(net.loc[valid])
        ex = net.loc[valid] - bench_net.loc[valid]
        p_cagr.append(s.cagr)
        p_sh.append(s.sharpe)
        p_ex.append(summarize(ex).sharpe)
        ex_cols.append(ex.rename(str(len(ex_cols))))
    if not ex_cols:
        raise RuntimeError("no complete CPCV path could be built (too little data or all splits skipped)")
    bsum = summarize(bench_net.loc[valid])
    ex_mat = pd.concat(ex_cols, axis=1).dropna()
    med = int(np.argsort(p_ex)[len(p_ex) // 2])
    dsr = deflated_sharpe_ratio(ex_mat.iloc[:, med].to_numpy(), max(n_trials, 1), var_sr_trials)
    spa_p = spa_test(ex_mat.to_numpy(), n_boot=500, seed=seed).p_value_spa if len(ex_mat) >= 20 else float("nan")
    fp = hashlib.sha256(np.round(xv[:2000], 8).tobytes() + str((kind, meta_labeling, n_groups, horizon)).encode()).hexdigest()[:16]
    res = CPCVModelResult(kind, meta_labeling, len(p_sh), p_cagr, p_sh, p_ex, bsum.cagr, bsum.sharpe, dsr, spa_p,
                          leakage_clean, n_trials, fingerprint=fp)
    return judge(res)
