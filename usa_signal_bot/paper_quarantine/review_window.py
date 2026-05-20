import datetime

from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate
from usa_signal_bot.core.enums import QuarantineCandidateStatus

def default_review_due_at(days: int = 7) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    due = now + datetime.timedelta(days=days)
    return due.isoformat()

def quarantine_review_expired(review_due_at_utc: str | None, now_utc: str | None = None) -> bool:
    if not review_due_at_utc:
        return False

    try:
        due_dt = datetime.datetime.fromisoformat(review_due_at_utc)
        now_dt = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(datetime.timezone.utc)
        return now_dt > due_dt
    except ValueError:
        return False

def review_window_warnings(candidate: QuarantinedPaperCandidate) -> list[str]:
    warnings = []
    if quarantine_review_expired(candidate.review_due_at_utc):
        warnings.append("Quarantine review window has expired.")
    return warnings

def extend_review_window(candidate: QuarantinedPaperCandidate, days: int = 7) -> QuarantinedPaperCandidate:
    if not candidate.review_due_at_utc:
        candidate.review_due_at_utc = default_review_due_at(days)
    else:
        try:
            current_due = datetime.datetime.fromisoformat(candidate.review_due_at_utc)
            new_due = current_due + datetime.timedelta(days=days)
            candidate.review_due_at_utc = new_due.isoformat()
        except ValueError:
             candidate.review_due_at_utc = default_review_due_at(days)

    if candidate.status == QuarantineCandidateStatus.EXPIRED and not quarantine_review_expired(candidate.review_due_at_utc):
         candidate.status = QuarantineCandidateStatus.WAITING_MANUAL_REVIEW

    return candidate

def review_window_to_text(candidate: QuarantinedPaperCandidate) -> str:
    expired = quarantine_review_expired(candidate.review_due_at_utc)
    lines = [
        f"Review Due At: {candidate.review_due_at_utc}",
        f"Is Expired: {expired}",
    ]
    return "\n".join(lines)
