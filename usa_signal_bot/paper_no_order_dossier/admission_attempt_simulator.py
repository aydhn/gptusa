from typing import Any
import json
from usa_signal_bot.core.enums import PaperAdmissionAttemptType
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    PaperAdmissionBlockerEvent,
    paper_admission_blocker_event_to_dict
)
from usa_signal_bot.paper_no_order_dossier.final_paper_admission_blocker import FinalPaperAdmissionBlocker
from usa_signal_bot.paper_no_order_dossier.admission_blocker_rules import dangerous_paper_admission_attempt_types

def _get_blocker(blocker: FinalPaperAdmissionBlocker | None = None) -> FinalPaperAdmissionBlocker:
    return blocker if blocker is not None else FinalPaperAdmissionBlocker()

def simulate_enable_active_paper_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.ENABLE_ACTIVE_PAPER, {"mode": "live"}, "simulator")

def simulate_enable_paper_runtime_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.ENABLE_PAPER_RUNTIME, {"runtime": "paper"}, "simulator")

def simulate_admit_candidate_to_paper_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.ADMIT_CANDIDATE_TO_PAPER, {"candidate_id": "simulated"}, "simulator")

def simulate_create_paper_session_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.CREATE_PAPER_SESSION, {}, "simulator")

def simulate_create_paper_order_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.CREATE_PAPER_ORDER, {"ticker": "AAPL"}, "simulator")

def simulate_commit_paper_state_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.COMMIT_PAPER_STATE, {"state": "changed"}, "simulator")

def simulate_patch_paper_config_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.PATCH_PAPER_CONFIG, {"config": "new"}, "simulator")

def simulate_send_broker_order_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.SEND_BROKER_ORDER, {"broker": "alpaca"}, "simulator")

def simulate_send_telegram_real_attempt(blocker: FinalPaperAdmissionBlocker | None = None) -> PaperAdmissionBlockerEvent:
    b = _get_blocker(blocker)
    return b.evaluate_attempt(PaperAdmissionAttemptType.SEND_TELEGRAM_REAL, {"message": "hello"}, "simulator")

def simulate_paper_admission_attempts(blocker: FinalPaperAdmissionBlocker | None = None) -> list[PaperAdmissionBlockerEvent]:
    b = _get_blocker(blocker)
    events = []
    for t in dangerous_paper_admission_attempt_types():
        events.append(b.evaluate_attempt(t, {"simulated": True}, "simulator_all"))
    return events

def paper_admission_attempt_simulator_summary(events: list[PaperAdmissionBlockerEvent]) -> dict[str, Any]:
    return {
        "simulated_count": len(events),
        "all_blocked": all(e.blocked for e in events)
    }

def paper_admission_attempt_simulator_to_text(events: list[PaperAdmissionBlockerEvent], limit: int = 100) -> str:
    return json.dumps([paper_admission_blocker_event_to_dict(e) for e in events[:limit]], indent=2)
