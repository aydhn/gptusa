from typing import Any
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    FinalPaperModeDryAdmissionGate,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle,
    DryAdmissionGateFullReview
)

def dry_admission_gate_from_board_dossier(payload: dict[str, Any]) -> FinalPaperModeDryAdmissionGate:
    from usa_signal_bot.paper_mode_dry_admission_gate.final_dry_admission_gate import build_default_final_dry_admission_gate
    return build_default_final_dry_admission_gate()

def shadow_replay_result_from_board_dossier(payload: dict[str, Any]) -> ShadowLaunchReplayResult:
    from usa_signal_bot.paper_mode_dry_admission_gate.shadow_replay_plan import build_default_shadow_replay_plan
    from usa_signal_bot.paper_mode_dry_admission_gate.shadow_replay_engine import ShadowLaunchBlockerReplayEngine
    plan = build_default_shadow_replay_plan()
    engine = ShadowLaunchBlockerReplayEngine()
    return engine.replay(plan, [])

def board_evidence_freeze_from_board_dossier(payload: dict[str, Any]) -> BoardEvidenceFreezeBundle:
    from usa_signal_bot.paper_mode_dry_admission_gate.board_evidence_freeze import build_board_evidence_freeze_bundle
    return build_board_evidence_freeze_bundle(payload)

def dry_admission_full_review_from_board_dossier(payload: dict[str, Any]) -> DryAdmissionGateFullReview:
    from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_report import build_dry_admission_gate_full_review
    return build_dry_admission_gate_full_review(payload)

def attach_dry_admission_metadata_to_board_dossier_payload(payload: dict[str, Any], review: DryAdmissionGateFullReview) -> dict[str, Any]:
    from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_report import dry_admission_gate_full_review_summary
    new_payload = payload.copy()
    new_payload["dry_admission_metadata"] = dry_admission_gate_full_review_summary(review)
    return new_payload

def board_dossier_dry_admission_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("dry_admission_metadata", {})

def board_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = board_dossier_dry_admission_summary(payload)
    return f"Board Dossier Adapter Summary: {summary}"
