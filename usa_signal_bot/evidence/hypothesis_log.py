"""Append-only JSONL hypothesis log: every evaluated strategy candidate is a trial, so selection-bias corrections
(DSR, SPA) can use the CUMULATIVE number of trials, not just the current run.

Time is injected for determinism. Writes are single-line appends; the log never rewrites past entries.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Dict, List


@dataclass
class HypothesisEntry:
    run_id: str
    logged_at: str
    family: str
    params: Dict[str, float]
    n_obs: int
    sharpe_per_period: float
    data_label: str = ""
    notes: List[str] = field(default_factory=list)


class HypothesisLog:
    def __init__(self, path: Path, clock: Callable[[], str]):
        self.path = Path(path)
        self._clock = clock

    def append(self, run_id: str, family: str, params: Dict[str, float], n_obs: int, sharpe: float, data_label: str = "") -> HypothesisEntry:
        e = HypothesisEntry(run_id, self._clock(), family, dict(params), int(n_obs), float(sharpe), data_label)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(e), sort_keys=True) + "\n")
        return e

    def entries(self) -> List[HypothesisEntry]:
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(HypothesisEntry(**json.loads(line)))
        return out

    def n_trials(self, data_label: str = "") -> int:
        """Distinct (family, params) candidates ever evaluated (optionally on one data label)."""
        seen = {(e.family, json.dumps(e.params, sort_keys=True)) for e in self.entries() if not data_label or e.data_label == data_label}
        return len(seen)

    def sharpe_variance(self, data_label: str = "") -> float:
        by = {}
        for e in self.entries():
            if not data_label or e.data_label == data_label:
                by[(e.family, json.dumps(e.params, sort_keys=True))] = e.sharpe_per_period
        vals = list(by.values())
        if len(vals) < 2:
            return 0.0
        m = sum(vals) / len(vals)
        return sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
