"""Combinatorial Purged Cross-Validation (Lopez de Prado, AFML ch.12): N groups, k test groups per split."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from math import comb
from typing import Iterator, List, Tuple

import numpy as np


@dataclass(frozen=True)
class CombinatorialPurgedCV:
    n_groups: int = 6
    n_test_groups: int = 2
    horizon: int = 5  # label at t uses data through t + horizon
    embargo: int = 5  # bars dropped from train after each test group

    @property
    def n_splits(self) -> int:
        return comb(self.n_groups, self.n_test_groups)

    @property
    def n_paths(self) -> int:
        return self.n_splits * self.n_test_groups // self.n_groups

    def _bounds(self, n_samples: int) -> np.ndarray:
        if not 1 <= self.n_test_groups < self.n_groups:
            raise ValueError("need 1 <= n_test_groups < n_groups")
        if n_samples < self.n_groups * 2:
            raise ValueError("not enough samples for the requested number of groups")
        return np.linspace(0, n_samples, self.n_groups + 1, dtype=int)

    def split(self, n_samples: int) -> Iterator[Tuple[np.ndarray, np.ndarray, Tuple[int, ...]]]:
        bounds = self._bounds(n_samples)
        idx = np.arange(n_samples)
        for combo in itertools.combinations(range(self.n_groups), self.n_test_groups):
            test_mask = np.zeros(n_samples, dtype=bool)
            drop = np.zeros(n_samples, dtype=bool)
            for g in combo:
                t0, t1 = bounds[g], bounds[g + 1]
                test_mask[t0:t1] = True
                # purge: train i with label window [i, i+h] touching [t0, t1); embargo after the block
                drop |= (idx + self.horizon >= t0) & (idx < t1 + self.embargo)
            yield idx[~drop & ~test_mask], idx[test_mask], combo

    def paths(self) -> List[List[Tuple[int, ...]]]:
        """Assign each (split, test-group) to a backtest path: every group appears once per path."""
        combos = list(itertools.combinations(range(self.n_groups), self.n_test_groups))
        used = {g: 0 for g in range(self.n_groups)}
        paths: List[List[Tuple[int, ...]]] = [[] for _ in range(self.n_paths)]
        for ci, combo in enumerate(combos):
            for g in combo:
                paths[used[g]].append((ci, g))
                used[g] += 1
        return paths


def assert_cpcv_no_leakage(train: np.ndarray, test: np.ndarray, horizon: int, embargo: int) -> None:
    """Raise if any train label window overlaps any contiguous test run or its embargo."""
    if len(train) == 0 or len(test) == 0:
        raise AssertionError("empty split")
    breaks = np.where(np.diff(test) > 1)[0]
    starts = np.concatenate([[test[0]], test[breaks + 1]])
    ends = np.concatenate([test[breaks], [test[-1]]])
    for t0, t1 in zip(starts, ends):
        bad = train[(train <= t1 + embargo) & (train + horizon >= t0)]
        if len(bad):
            raise AssertionError(f"train sample {int(bad[0])} overlaps test run [{t0},{t1}]")
