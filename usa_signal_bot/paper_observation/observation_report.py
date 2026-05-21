from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import (
    ObservationWindow, ObservationTelemetrySummary, CheckpointHistoryEntry,
    QuarantineExitReview, ObservationReview, ObservationReportType, create_quarantine_exit_review_id, create_observation_review_id
)
import datetime
from usa_signal_bot.paper_observation.observation_scoring import build_observation_scorecard
from usa_signal_bot.paper_observation.exit_decision_board import QuarantineExitDecisionBoard
from usa_signal_bot.paper_observation.exit_gates import default_quarantine_exit_gates
from usa_signal_bot.paper_observation.exit_audit import audit_entry_from_exit_review
from usa_signal_bot.paper_observation.observation_reporting import observation_limitations_text

def build_quarantine_exit_review(
    window: ObservationWindow,
    telemetry: ObservationTelemetrySummary,
    checkpoint_entries: List[CheckpointHistoryEntry],
    dry_run_sessions: List[dict[str, Any]] | None = None
) -> QuarantineExitReview:

    scorecard = build_observation_scorecard(window, telemetry, checkpoint_entries, dry_run_sessions)
    gates = default_quarantine_exit_gates(window, telemetry, checkpoint_entries, dry_run_sessions or [])

    board = QuarantineExitDecisionBoard()
    decision = board.decide(scorecard, gates)

    return QuarantineExitReview(
        exit_review_id=create_quarantine_exit_review_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        window_id=window.window_id,
        candidate_id=window.candidate_id,
        ticket_id=window.ticket_id,
        decision=decision,
        scorecard=scorecard,
        telemetry_summary=telemetry,
        checkpoint_history=checkpoint_entries,
        risk_flags=scorecard.risk_flags,
        rationale=f"Decision based on score {scorecard.score} and risk flags {len(scorecard.risk_flags)}.",
        required_followups=[],
        manual_review_required=scorecard.manual_review_required,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def build_observation_review(
    window: ObservationWindow,
    dry_run_payload: dict[str, Any] | None = None,
    quarantine_payload: dict[str, Any] | None = None
) -> ObservationReview:

    # Mocking telemetry and entries for standalone build capability
    telemetry = ObservationTelemetrySummary("ts1", datetime.datetime.now(datetime.timezone.utc).isoformat(), window.window_id, window.candidate_id, 0, 0, 0, 0, 0, 0, 0, 0)
    entries = []

    exit_review = build_quarantine_exit_review(window, telemetry, entries, dry_run_payload.get("sessions", []) if dry_run_payload else None)
    audit_entry = audit_entry_from_exit_review(exit_review)

    return ObservationReview(
        review_id=create_observation_review_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        report_type=ObservationReportType.FULL_OBSERVATION_REVIEW,
        windows=[window],
        telemetry_summaries=[telemetry],
        checkpoint_history=entries,
        scorecards=[exit_review.scorecard] if exit_review.scorecard else [],
        exit_reviews=[exit_review],
        audit_entries=[audit_entry],
        output_paths={},
        warnings=[],
        errors=[]
    )

def observation_review_summary(review: ObservationReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "type": review.report_type,
        "exit_decision": review.exit_reviews[-1].decision if review.exit_reviews else "UNKNOWN"
    }

def observation_review_to_text(review: ObservationReview, limit: int = 100) -> str:
    lines = [f"Observation Review {review.review_id}", observation_limitations_text()]
    return "\n".join(lines)
