"""Connects drift-monitoring results to the offline model registry (request a retrain candidate only).

Nothing here trains, activates or routes anything. A trigger yields a ``RetrainRequest`` that is recorded in the
registry as a CANDIDATE with ``activation_allowed=False``; moving it forward still needs the normal promotion gate
and ``ModelRegistry.approve`` (human). Results are duck-typed (``.severity``) so this does not import ml_research.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from usa_signal_bot.ml_loop.registry import ModelRecord, ModelRegistry

_ORDER = {"NONE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "BLOCKING": 4}


def _sev(item) -> str:
    s = getattr(item, "severity", None)
    return str(getattr(s, "value", s) or "NONE").upper()


@dataclass(frozen=True)
class RetrainPolicy:
    min_severity: str = "HIGH"  # any metric at/above this triggers
    min_medium_count: int = 3  # or this many MEDIUM-or-worse metrics


@dataclass
class RetrainRequest:
    triggered: bool
    reasons: List[str] = field(default_factory=list)
    activation_allowed: bool = False


def evaluate_retrain(results: Iterable, policy: Optional[RetrainPolicy] = None) -> RetrainRequest:
    policy = policy or RetrainPolicy()
    items = list(results)
    threshold = _ORDER.get(policy.min_severity.upper(), 3)
    reasons: List[str] = []
    for it in items:
        if _ORDER.get(_sev(it), 0) >= threshold:
            reasons.append(f"{getattr(it, 'metric_name', 'metric')}: {_sev(it)}")
    medium = sum(1 for it in items if _ORDER.get(_sev(it), 0) >= 2)
    if not reasons and medium >= policy.min_medium_count:
        reasons.append(f"{medium} metrics at MEDIUM or worse")
    return RetrainRequest(triggered=bool(reasons), reasons=reasons)


def register_retrain_candidate(
    registry: ModelRegistry, model_id: str, request: RetrainRequest, data_fingerprint: str
) -> Optional[ModelRecord]:
    """Record a retrain request as a CANDIDATE placeholder (no metrics => the gate will reject until retrained)."""
    if not request.triggered:
        return None
    rec = registry.register(model_id, {"retrain_reasons": float(len(request.reasons))}, {}, data_fingerprint, leakage_clean=False)
    assert rec.activation_allowed is False
    return rec
