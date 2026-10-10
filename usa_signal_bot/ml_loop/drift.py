"""Feature drift (Population Stability Index) feeding ``retrain_trigger`` - a real input instead of a placeholder.

Results expose ``metric_name`` and ``severity`` exactly like the duck-typed items ``evaluate_retrain`` reads, and the
trigger also understands ``ml_research.drift_monitoring`` results (``drift_severity``/``calibration_severity``).
Nothing here trains or activates anything: a trigger only records a CANDIDATE placeholder (activation_allowed=False).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DriftResult:
    metric_name: str
    psi: float
    severity: str  # NONE | LOW | MEDIUM | HIGH


def psi(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Population Stability Index with reference-quantile bins (0.1 / 0.25 are the usual medium / high cut-offs)."""
    ref = np.asarray(reference, dtype=float)
    cur = np.asarray(current, dtype=float)
    ref, cur = ref[~np.isnan(ref)], cur[~np.isnan(cur)]
    if len(ref) < bins or len(cur) < bins:
        return float("nan")
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return 0.0
    edges[0], edges[-1] = -np.inf, np.inf
    p = np.histogram(ref, edges)[0] / len(ref)
    q = np.histogram(cur, edges)[0] / len(cur)
    p, q = np.clip(p, 1e-6, None), np.clip(q, 1e-6, None)
    return float(np.sum((q - p) * np.log(q / p)))


def severity_from_psi(value: float) -> str:
    if value != value:
        return "NONE"
    if value >= 0.25:
        return "HIGH"
    if value >= 0.10:
        return "MEDIUM"
    if value >= 0.05:
        return "LOW"
    return "NONE"


def feature_drift(reference: pd.DataFrame, current: pd.DataFrame) -> List[DriftResult]:
    out: List[DriftResult] = []
    for col in reference.columns:
        if col in current.columns:
            v = psi(reference[col].to_numpy(), current[col].to_numpy())
            out.append(DriftResult(f"psi:{col}", v, severity_from_psi(v)))
    return out
