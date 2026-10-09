"""Tiny numpy models (no third-party ML dependency)."""

from __future__ import annotations

import numpy as np


class RidgeModel:
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0
        self._mu: np.ndarray | None = None
        self._sd: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> "RidgeModel":
        self._mu = x.mean(axis=0)
        self._sd = x.std(axis=0)
        self._sd[self._sd == 0] = 1.0
        z = (x - self._mu) / self._sd
        self.intercept_ = float(y.mean())
        yc = y - self.intercept_
        a = z.T @ z + self.alpha * np.eye(z.shape[1])
        self.coef_ = np.linalg.solve(a, z.T @ yc)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("model not fitted")
        return ((x - self._mu) / self._sd) @ self.coef_ + self.intercept_


class MeanBaseline:
    """Predicts the training mean - the bar any model has to beat out-of-sample."""

    def fit(self, x: np.ndarray, y: np.ndarray) -> "MeanBaseline":
        self.mean_ = float(y.mean())
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.full(len(x), self.mean_)
