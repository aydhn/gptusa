from typing import Any
from .simulator_gate_models import SimulatorGateFullReview, FinalLocalPaperAdmissionSimulatorGate, RehearsalReplayResult, DryAdmissionEvidenceFreezeBundle, create_simulator_full_review_id
from usa_signal_bot.core.enums import SimulatorGateReportType
from datetime import datetime, timezone

def build_simulator_gate_full_review(payload: dict[str, Any]) -> SimulatorGateFullReview:
    return SimulatorGateFullReview(
        review_id=create_simulator_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=SimulatorGateReportType.FULL_SIMULATOR_GATE_REVIEW
    )

def build_simulator_review_from_parts(gate: FinalLocalPaperAdmissionSimulatorGate, replay_result: RehearsalReplayResult | None = None, freeze_bundle: DryAdmissionEvidenceFreezeBundle | None = None) -> SimulatorGateFullReview:
    return SimulatorGateFullReview(
        review_id=create_simulator_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=SimulatorGateReportType.FULL_SIMULATOR_GATE_REVIEW,
        gates=[gate],
        rehearsal_replay_results=[replay_result] if replay_result else [],
        evidence_freezes=[freeze_bundle] if freeze_bundle else []
    )

def simulator_gate_full_review_summary(review: SimulatorGateFullReview) -> dict[str, Any]:
    return {}

def simulator_gate_limitations_text() -> str:
    return ""

def simulator_gate_full_review_to_text(review: SimulatorGateFullReview, limit: int = 100) -> str:
    return ""
