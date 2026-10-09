"""File-backed model registry with a controlled promotion gate.

Lifecycle: CANDIDATE -> (gate passes) ELIGIBLE -> (explicit human approval) APPROVED_FOR_RESEARCH.
There is no automatic activation: ``activation_allowed`` stays False for every record and nothing here
connects to a trading path. Time is injected (``clock``) for determinism.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

from usa_signal_bot.paper_common.io import write_json

CANDIDATE, ELIGIBLE, APPROVED = "CANDIDATE", "ELIGIBLE", "APPROVED_FOR_RESEARCH"
REJECTED = "REJECTED"


@dataclass
class PromotionThresholds:
    min_ic: float = 0.02  # mean out-of-fold rank IC
    min_ic_gain_over_baseline: float = 0.02
    min_positive_fold_fraction: float = 0.6
    require_clean_leakage: bool = True
    min_dsr: Optional[float] = None  # optional selection-bias gate; needs metrics['dsr'] when set


@dataclass
class ModelRecord:
    model_id: str
    created_at: str
    params: Dict[str, float]
    metrics: Dict[str, float]
    data_fingerprint: str
    leakage_clean: bool
    status: str = CANDIDATE
    gate_reasons: List[str] = field(default_factory=list)
    approved_by: Optional[str] = None
    approval_note: Optional[str] = None
    activation_allowed: bool = False  # never set True by this module


class ModelRegistry:
    def __init__(self, root: Path, clock: Callable[[], str]):
        self.root = Path(root)
        self._clock = clock

    def _path(self, model_id: str) -> Path:
        return self.root / f"{model_id}.json"

    def register(self, model_id: str, params: Dict[str, float], metrics: Dict[str, float], data_fingerprint: str, leakage_clean: bool) -> ModelRecord:
        if self._path(model_id).exists():
            raise FileExistsError(f"model '{model_id}' already registered")
        rec = ModelRecord(model_id, self._clock(), params, metrics, data_fingerprint, leakage_clean)
        write_json(self._path(model_id), asdict(rec))
        return rec

    def get(self, model_id: str) -> ModelRecord:
        data = json.loads(self._path(model_id).read_text(encoding="utf-8"))
        return ModelRecord(**data)

    def _save(self, rec: ModelRecord) -> None:
        write_json(self._path(rec.model_id), asdict(rec))

    def evaluate_promotion(self, model_id: str, th: PromotionThresholds) -> ModelRecord:
        """Run the gate. Passing only makes the model ELIGIBLE; a human still has to approve it."""
        rec = self.get(model_id)
        reasons: List[str] = []
        m = rec.metrics
        if th.require_clean_leakage and not rec.leakage_clean:
            reasons.append("leakage check not clean")
        if m.get("oos_ic_mean", float("-inf")) < th.min_ic:
            reasons.append(f"oos_ic_mean {m.get('oos_ic_mean')} < {th.min_ic}")
        if m.get("oos_ic_mean", 0.0) - m.get("baseline_ic_mean", 0.0) < th.min_ic_gain_over_baseline:
            reasons.append("gain over baseline too small")
        if m.get("positive_fold_fraction", 0.0) < th.min_positive_fold_fraction:
            reasons.append("too few positive folds")
        if th.min_dsr is not None and m.get("dsr", float("-inf")) < th.min_dsr:
            reasons.append(f"dsr {m.get('dsr')} < {th.min_dsr}")
        rec.gate_reasons = reasons
        rec.status = ELIGIBLE if not reasons else REJECTED
        self._save(rec)
        return rec

    def approve(self, model_id: str, approver: str, note: str) -> ModelRecord:
        """Human approval. Requires status ELIGIBLE, a named approver and a note."""
        if not approver.strip() or not note.strip():
            raise ValueError("approver and note are required")
        rec = self.get(model_id)
        if rec.status != ELIGIBLE:
            raise PermissionError(f"model '{model_id}' is {rec.status}; only ELIGIBLE models can be approved")
        rec.status = APPROVED
        rec.approved_by = approver
        rec.approval_note = note
        self._save(rec)
        return rec

    def list_ids(self) -> List[str]:
        return sorted(p.stem for p in self.root.glob("*.json")) if self.root.exists() else []
