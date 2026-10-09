"""Selection-bias statistics: PSR, expected max Sharpe, DSR (Bailey & Lopez de Prado 2012/2014) and PBO via CSCV
(Bailey, Borwein, Lopez de Prado, Zhu 2017).

All Sharpe ratios here are per-period (NOT annualised) unless stated; annualise outside.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from statistics import NormalDist
from typing import Optional, Sequence

import numpy as np

_N = NormalDist()
EULER_GAMMA = 0.5772156649015329


def sample_moments(returns: np.ndarray) -> tuple[float, float, float, int]:
    """(per-period Sharpe, skewness, kurtosis [non-excess], n)."""
    r = np.asarray(returns, dtype=float)
    r = r[~np.isnan(r)]
    n = len(r)
    if n < 4:
        raise ValueError("need at least 4 observations")
    sd = r.std(ddof=1)
    if sd == 0:
        return 0.0, 0.0, 3.0, n
    z = (r - r.mean()) / r.std(ddof=0)
    return float(r.mean() / sd), float(np.mean(z**3)), float(np.mean(z**4)), n


def probabilistic_sharpe_ratio(sr: float, sr_benchmark: float, n_obs: int, skew: float = 0.0, kurt: float = 3.0) -> float:
    """P(true SR > sr_benchmark) given estimate ``sr`` over ``n_obs`` observations (non-normal aware)."""
    denom = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr**2
    if denom <= 0 or n_obs < 2:
        return float("nan")
    return _N.cdf((sr - sr_benchmark) * math.sqrt(n_obs - 1) / math.sqrt(denom))


def expected_max_sharpe(n_trials: int, n_obs: int, var_sr: Optional[float] = None) -> float:
    """Expected maximum per-period Sharpe among ``n_trials`` independent zero-skill trials.

    ``var_sr`` is the cross-trial variance of Sharpe estimates; when omitted it is the sampling variance under the
    null SR=0, 1/(n_obs-1), so the threshold shrinks as the sample length grows.
    """
    if n_trials < 1:
        raise ValueError("n_trials must be >= 1")
    if var_sr is None:
        if n_obs < 2:
            raise ValueError("n_obs must be >= 2")
        var_sr = 1.0 / (n_obs - 1)
    if n_trials == 1:
        return 0.0
    g = EULER_GAMMA
    return math.sqrt(var_sr) * ((1 - g) * _N.inv_cdf(1 - 1.0 / n_trials) + g * _N.inv_cdf(1 - 1.0 / (n_trials * math.e)))


def deflated_sharpe_ratio(returns: np.ndarray, n_trials: int, var_sr_trials: Optional[float] = None) -> float:
    """DSR: PSR evaluated against the expected-max Sharpe of ``n_trials`` trials (selection-bias corrected)."""
    sr, skew, kurt, n = sample_moments(returns)
    sr0 = expected_max_sharpe(n_trials, n, var_sr_trials)
    return probabilistic_sharpe_ratio(sr, sr0, n, skew, kurt)


@dataclass(frozen=True)
class PBOResult:
    pbo: float
    n_combinations: int
    logits: tuple


def _sharpe_cols(m: np.ndarray) -> np.ndarray:
    sd = m.std(axis=0, ddof=1)
    out = np.zeros(m.shape[1])
    ok = sd > 0
    out[ok] = m.mean(axis=0)[ok] / sd[ok]
    return out


def pbo_cscv(returns: np.ndarray, n_blocks: int = 8) -> PBOResult:
    """Probability of Backtest Overfitting via CSCV.

    ``returns``: (T, N) matrix of strategy-trial returns. Splits T into ``n_blocks`` (even) contiguous blocks, uses
    every C(S, S/2) in-sample/out-of-sample partition; PBO = share of partitions where the in-sample best trial ranks
    at or below the OOS median (logit <= 0).
    """
    m = np.asarray(returns, dtype=float)
    if m.ndim != 2 or m.shape[1] < 2:
        raise ValueError("returns must be (T, N>=2)")
    if n_blocks < 2 or n_blocks % 2:
        raise ValueError("n_blocks must be even and >= 2")
    t, n = m.shape
    if t < n_blocks * 2:
        raise ValueError("too few observations for n_blocks")
    blocks = np.array_split(np.arange(t), n_blocks)
    logits = []
    for is_ids in itertools.combinations(range(n_blocks), n_blocks // 2):
        oos_ids = [b for b in range(n_blocks) if b not in is_ids]
        is_idx = np.concatenate([blocks[b] for b in is_ids])
        oos_idx = np.concatenate([blocks[b] for b in oos_ids])
        best = int(np.argmax(_sharpe_cols(m[is_idx])))
        oos = _sharpe_cols(m[oos_idx])
        rank = (oos < oos[best]).sum() + 1 + 0.5 * ((oos == oos[best]).sum() - 1)  # average rank, 1..N
        w = rank / (n + 1)
        logits.append(math.log(w / (1 - w)))
    arr = np.array(logits)
    return PBOResult(float((arr <= 0).mean()), len(logits), tuple(float(x) for x in arr))


def trial_sharpe_variance(returns: Sequence[np.ndarray]) -> float:
    """Cross-trial variance of per-period Sharpe estimates (input for DSR)."""
    srs = [sample_moments(np.asarray(r))[0] for r in returns]
    return float(np.var(srs, ddof=1)) if len(srs) > 1 else 0.0
