"""White's Reality Check and Hansen's Superior Predictive Ability (SPA) test with a stationary bootstrap.

Question answered: given K candidate strategies, is the BEST one's outperformance over the benchmark real, after
accounting for having looked at K candidates? Input: (T, K) matrix of excess returns (strategy - benchmark).
References: White (2000) Econometrica; Hansen (2005) JBES; Politis & Romano (1994) stationary bootstrap.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SPAResult:
    p_value_rc: float  # White's Reality Check (null centred at 0 for all models)
    p_value_spa: float  # Hansen SPA, consistent recentring
    best_index: int
    best_mean: float  # per-period mean excess return of the best model
    n_obs: int
    n_models: int


def stationary_bootstrap_indices(n: int, n_boot: int, mean_block: float, rng: np.random.Generator) -> np.ndarray:
    """(n_boot, n) index matrix; blocks have geometric length with mean ``mean_block``."""
    p = 1.0 / max(mean_block, 1.0)
    idx = np.empty((n_boot, n), dtype=np.int64)
    idx[:, 0] = rng.integers(0, n, size=n_boot)
    jump = rng.random((n_boot, n)) < p
    starts = rng.integers(0, n, size=(n_boot, n))
    for t in range(1, n):
        idx[:, t] = np.where(jump[:, t], starts[:, t], (idx[:, t - 1] + 1) % n)
    return idx


def spa_test(excess: np.ndarray, n_boot: int = 1000, mean_block: float = 10.0, seed: int = 0) -> SPAResult:
    d = np.asarray(excess, dtype=float)
    if d.ndim != 2 or d.shape[1] < 1 or d.shape[0] < 20:
        raise ValueError("excess must be (T>=20, K>=1)")
    d = d[~np.isnan(d).any(axis=1)]
    n, k = d.shape
    mean = d.mean(axis=0)
    rng = np.random.default_rng(seed)
    idx = stationary_bootstrap_indices(n, n_boot, mean_block, rng)
    boot_means = d[idx].mean(axis=1)  # (n_boot, k)
    centred = boot_means - mean  # bootstrap distribution around the sample mean
    omega = np.sqrt(np.maximum((np.sqrt(n) * centred).var(axis=0, ddof=1), 1e-24))  # per-model std of sqrt(n)*mean
    t_stat = np.sqrt(n) * mean / omega
    # White's RC: statistic = max sqrt(n)*mean (non-studentised), null centred at 0
    v_rc = max(np.sqrt(n) * mean.max(), 0.0)
    v_rc_boot = (np.sqrt(n) * centred).max(axis=1)
    p_rc = float((v_rc_boot >= v_rc).mean())
    # Hansen SPA: studentised statistic, recentre only models that are not clearly inferior
    v_spa = max(t_stat.max(), 0.0)
    thresh = -np.sqrt(2.0 * np.log(np.log(n)))
    mu_c = np.where(t_stat >= thresh, 0.0, mean)  # poor models are pushed to mean (kept negative) so they cannot drive the max
    recentred = (boot_means - mean + mu_c)  # E* = mu_c
    v_spa_boot = np.maximum((np.sqrt(n) * recentred / omega).max(axis=1), 0.0)
    p_spa = float((v_spa_boot >= v_spa).mean())
    best = int(np.argmax(t_stat))
    return SPAResult(p_rc, p_spa, best, float(mean[best]), n, k)
