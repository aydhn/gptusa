
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    FinalPaperSafeGate, BoundaryCertificateReplayResult, FrozenEvidenceIntegrityAudit,
    PaperSafeGateFullReview
)
from usa_signal_bot.paper_safe_gate.final_paper_safe_gate import build_default_final_paper_safe_gate
from usa_signal_bot.paper_safe_gate.boundary_replay_engine import BoundaryCertificateReplayEngine
from usa_signal_bot.paper_safe_gate.boundary_replay_plan import build_default_boundary_replay_plan
from usa_signal_bot.paper_safe_gate.frozen_evidence_integrity import build_frozen_evidence_integrity_audit
from usa_signal_bot.paper_safe_gate.paper_safe_report import build_paper_safe_review_from_parts

def paper_safe_gate_from_boundary(payload: Dict[str, Any]) -> FinalPaperSafeGate:
    return build_default_final_paper_safe_gate()

def boundary_replay_result_from_boundary(payload: Dict[str, Any]) -> BoundaryCertificateReplayResult:
    engine = BoundaryCertificateReplayEngine()
    plan = build_default_boundary_replay_plan()
    return engine.replay(plan, payload)

def frozen_evidence_integrity_from_boundary(payload: Dict[str, Any]) -> FrozenEvidenceIntegrityAudit:
    return build_frozen_evidence_integrity_audit(payload)

def paper_safe_full_review_from_boundary(payload: Dict[str, Any]) -> PaperSafeGateFullReview:
    gate = paper_safe_gate_from_boundary(payload)
    return build_paper_safe_review_from_parts(gate)

def attach_paper_safe_metadata_to_boundary_payload(payload: Dict[str, Any], review: PaperSafeGateFullReview) -> Dict[str, Any]:
    payload["paper_safe_gate"] = review.review_id
    return payload

def boundary_paper_safe_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"boundary_attached": True}

def boundary_adapter_to_text(payload: Dict[str, Any]) -> str:
    return "Boundary Adapter Success"
