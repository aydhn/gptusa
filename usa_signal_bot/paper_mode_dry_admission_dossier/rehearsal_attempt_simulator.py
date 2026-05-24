from typing import Any
from usa_signal_bot.core.enums import PaperModeRehearsalAttemptType
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import PaperModeRehearsalBlockerEvent
from usa_signal_bot.paper_mode_dry_admission_dossier.final_rehearsal_blocker import FinalPaperModeRehearsalBlocker
from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_blocker_rules import dangerous_rehearsal_attempt_types

def _sim_attempt(blocker: FinalPaperModeRehearsalBlocker | None, attempt_type: PaperModeRehearsalAttemptType) -> PaperModeRehearsalBlockerEvent:
    b = blocker or FinalPaperModeRehearsalBlocker()
    return b.evaluate_attempt(attempt_type, {"simulated": True}, "simulator")

def simulate_start_paper_mode_rehearsal_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.START_PAPER_MODE_REHEARSAL)

def simulate_start_local_paper_rehearsal_runtime_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.START_LOCAL_PAPER_REHEARSAL_RUNTIME)

def simulate_rehearse_candidate_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.REHEARSE_CANDIDATE)

def simulate_admit_candidate_to_rehearsal_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.ADMIT_CANDIDATE_TO_REHEARSAL)

def simulate_create_rehearsal_session_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.CREATE_REHEARSAL_SESSION)

def simulate_create_paper_session_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.CREATE_PAPER_SESSION)

def simulate_create_paper_order_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.CREATE_PAPER_ORDER)

def simulate_commit_paper_state_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.COMMIT_PAPER_STATE)

def simulate_patch_paper_config_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.PATCH_PAPER_CONFIG)

def simulate_send_broker_order_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.SEND_BROKER_ORDER)

def simulate_send_telegram_real_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.SEND_TELEGRAM_REAL)

def simulate_unlock_rehearsal_gate_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.UNLOCK_REHEARSAL_GATE)

def simulate_rehearsal_attempts(blocker: FinalPaperModeRehearsalBlocker | None = None) -> list[PaperModeRehearsalBlockerEvent]:
    b = blocker or FinalPaperModeRehearsalBlocker()
    return [_sim_attempt(b, t) for t in dangerous_rehearsal_attempt_types()]

def rehearsal_attempt_simulator_summary(events: list[PaperModeRehearsalBlockerEvent]) -> dict[str, Any]:
    return {
        "simulated": len(events),
        "blocked": sum(1 for e in events if e.blocked)
    }

def rehearsal_attempt_simulator_to_text(events: list[PaperModeRehearsalBlockerEvent], limit: int = 100) -> str:
    summary = rehearsal_attempt_simulator_summary(events)
    return f"Rehearsal Attempt Simulator: {summary['blocked']}/{summary['simulated']} blocked"
