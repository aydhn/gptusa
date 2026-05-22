from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWriteAdmissionFullReview, NoWritePaperAdmissionContract, ActivationReplayResult, PaperModePreflightRun
from usa_signal_bot.core.enums import NoWriteAdmissionReportType
import datetime

def build_no_write_admission_full_review(board_payload: dict[str, Any]) -> NoWriteAdmissionFullReview:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return NoWriteAdmissionFullReview(
        review_id="rev1", created_at_utc=now, report_type=NoWriteAdmissionReportType.FULL_NO_WRITE_ADMISSION_REVIEW,
        contracts=[], activation_replay_plans=[], activation_replay_results=[], preflight_runs=[], audit_entries=[],
        output_paths={}, warnings=[], errors=[]
    )

def build_no_write_admission_review_from_parts(contract: NoWritePaperAdmissionContract, replay_result: ActivationReplayResult | None = None, preflight: PaperModePreflightRun | None = None) -> NoWriteAdmissionFullReview:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return NoWriteAdmissionFullReview(
        review_id="rev1", created_at_utc=now, report_type=NoWriteAdmissionReportType.FULL_NO_WRITE_ADMISSION_REVIEW,
        contracts=[contract], activation_replay_plans=[], activation_replay_results=[replay_result] if replay_result else [], preflight_runs=[preflight] if preflight else [], audit_entries=[],
        output_paths={}, warnings=[], errors=[]
    )

def no_write_admission_full_review_summary(review: NoWriteAdmissionFullReview) -> dict[str, Any]:
    return {}

def no_write_admission_limitations_text() -> str:
    return "No write admission contract is not active paper admission."

def no_write_admission_full_review_to_text(review: NoWriteAdmissionFullReview, limit: int = 100) -> str:
    return "Full Review"
