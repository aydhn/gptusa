from typing import Any, Dict
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    PrePaperGovernanceCheckpoint,
    FinalHandoffFullReview
)
from usa_signal_bot.paper_final_handoff.final_handoff_report import build_final_handoff_review, build_final_handoff_full_review
from usa_signal_bot.paper_final_handoff.archive_manifest import build_sealed_readiness_archive_manifest
from usa_signal_bot.paper_final_handoff.archive_sealing import seal_readiness_archive
from usa_signal_bot.paper_final_handoff.archive_integrity import build_archive_integrity_report
from usa_signal_bot.paper_final_handoff.checkpoint_gates import default_pre_paper_checkpoint_gates
from usa_signal_bot.paper_final_handoff.checkpoint_decision import PrePaperCheckpointDecisionEngine

def final_handoff_review_from_readiness_rehearsal(payload: Dict[str, Any]) -> FinalHandoffReview:
    return build_final_handoff_review(payload)

def sealed_archive_from_readiness_rehearsal(payload: Dict[str, Any]) -> SealedReadinessArchiveManifest:
    review = final_handoff_review_from_readiness_rehearsal(payload)
    manifest = build_sealed_readiness_archive_manifest(review)
    return seal_readiness_archive(manifest)

def pre_paper_checkpoint_from_readiness_rehearsal(payload: Dict[str, Any]) -> PrePaperGovernanceCheckpoint:
    review = final_handoff_review_from_readiness_rehearsal(payload)
    manifest = sealed_archive_from_readiness_rehearsal(payload)
    integrity = build_archive_integrity_report(manifest)
    gates = default_pre_paper_checkpoint_gates(review, manifest, integrity)
    engine = PrePaperCheckpointDecisionEngine()
    return engine.decide(review, manifest, integrity, gates)

def final_handoff_full_review_from_readiness_rehearsal(payload: Dict[str, Any]) -> FinalHandoffFullReview:
    review = final_handoff_review_from_readiness_rehearsal(payload)
    manifest = build_sealed_readiness_archive_manifest(review)
    manifest = seal_readiness_archive(manifest)
    integrity = build_archive_integrity_report(manifest)
    gates = default_pre_paper_checkpoint_gates(review, manifest, integrity)
    engine = PrePaperCheckpointDecisionEngine()
    checkpoint = engine.decide(review, manifest, integrity, gates)
    return build_final_handoff_full_review(review, manifest, integrity, checkpoint)

def attach_final_handoff_metadata_to_readiness_payload(payload: Dict[str, Any], review: FinalHandoffFullReview) -> Dict[str, Any]:
    out = payload.copy()
    out["final_handoff_review_id"] = review.review_id
    return out

def readiness_rehearsal_final_handoff_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"id": payload.get("final_handoff_review_id")}

def readiness_rehearsal_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"ReadinessAdapter: {payload.get('final_handoff_review_id')}"
