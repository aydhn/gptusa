"""Purged K-fold with embargo for time-series samples whose labels span ``horizon`` future bars."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Tuple

import numpy as np


@dataclass(frozen=True)
class PurgedKFold:
    n_splits: int = 5
    horizon: int = 5  # label at t uses data through t + horizon
    embargo: int = 5  # extra bars dropped from train after each test block

    def split(self, n_samples: int) -> Iterator[Tuple[np.ndarray, np.ndarray]]:
        if self.n_splits < 2 or n_samples < self.n_splits * 2:
            raise ValueError("not enough samples for the requested number of splits")
        bounds = np.linspace(0, n_samples, self.n_splits + 1, dtype=int)
        idx = np.arange(n_samples)
        for k in range(self.n_splits):
            t0, t1 = bounds[k], bounds[k + 1]
            test = idx[t0:t1]
            # train sample i is kept only if its label window [i, i+horizon] does not touch the test
            # block, and it is not inside the embargo that follows the test block
            before = idx[idx + self.horizon < t0]
            after = idx[idx >= t1 + self.embargo]
            yield np.concatenate([before, after]), test


def assert_no_leakage(train: np.ndarray, test: np.ndarray, horizon: int, embargo: int) -> None:
    """Raise if any train label window overlaps the test block or its embargo."""
    if len(train) == 0 or len(test) == 0:
        raise AssertionError("empty split")
    t0, t1 = int(test.min()), int(test.max())
    for i in (train[(train <= t1 + embargo) & (train + horizon >= t0)]).tolist():
        raise AssertionError(f"train sample {i} overlaps test block [{t0},{t1}] (horizon={horizon}, embargo={embargo})")
