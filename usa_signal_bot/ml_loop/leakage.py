"""Leakage guards for feature/label frames (time-indexed, one row per decision date)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import pandas as pd


@dataclass
class LeakageReport:
    issues: List[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not self.issues


def check_leakage(features: pd.DataFrame, labels: pd.Series, horizon: int, suspicious_corr: float = 0.5) -> LeakageReport:
    """Static checks run before any training:

    * index monotonic, unique and aligned between features and labels;
    * no feature column that is (almost) identical to the label (target leak);
    * no feature that correlates far more strongly with the label when shifted *back* from the future
      (``feature.shift(-1)``) than at its own timestamp, which is the signature of forward-looking features;
    * no NaN labels remaining in the usable rows beyond the last ``horizon`` rows.
    """
    rep = LeakageReport()
    if not features.index.is_monotonic_increasing or not features.index.is_unique:
        rep.issues.append("feature index not strictly increasing")
    if not features.index.equals(labels.index):
        rep.issues.append("features and labels index differ")
        return rep
    usable = labels.iloc[: max(len(labels) - horizon, 0)]
    if usable.isna().any():
        rep.issues.append("NaN labels inside usable range")
    for col in features.columns:
        f = features[col]
        both = pd.concat([f, labels], axis=1).dropna()
        if len(both) < 30:
            continue
        same = both.iloc[:, 0].corr(both.iloc[:, 1])
        if same == same and abs(same) > 0.98:
            rep.issues.append(f"feature '{col}' ~ label (corr={same:.2f})")
        fwd = pd.concat([f.shift(-1), labels], axis=1).dropna()
        if len(fwd) >= 30:
            c_fwd = fwd.iloc[:, 0].corr(fwd.iloc[:, 1])
            if c_fwd == c_fwd and same == same and abs(c_fwd) > suspicious_corr and abs(c_fwd) > 2 * abs(same):
                rep.issues.append(f"feature '{col}' looks forward-looking (corr next-bar {c_fwd:.2f} vs {same:.2f})")
    return rep
