from typing import Any
from usa_signal_bot.core.enums import PaperSandboxRuntimeAdmissionAttemptType
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import PaperSandboxRuntimeAdmissionBlockerEvent
from usa_signal_bot.local_paper_admission_simulator_dossier.final_sandbox_runtime_admission_blocker import FinalPaperSandboxRuntimeAdmissionBlocker

def simulate_sandbox_runtime_admission_attempts(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> list[PaperSandboxRuntimeAdmissionBlockerEvent]:
    if not blocker:
        blocker = FinalPaperSandboxRuntimeAdmissionBlocker()

    events = [
        simulate_start_paper_sandbox_runtime_attempt(blocker),
        simulate_admit_candidate_to_sandbox_runtime_attempt(blocker),
        simulate_start_sandbox_paper_session_attempt(blocker),
        simulate_create_sandbox_paper_session_attempt(blocker),
        simulate_create_sandbox_paper_order_attempt(blocker),
        simulate_commit_sandbox_paper_state_attempt(blocker),
        simulate_patch_sandbox_runtime_config_attempt(blocker),
        simulate_send_sandbox_broker_order_attempt(blocker),
        simulate_send_sandbox_telegram_real_attempt(blocker),
        simulate_unlock_sandbox_runtime_admission_gate_attempt(blocker)
    ]
    return events

def simulate_start_paper_sandbox_runtime_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.START_PAPER_SANDBOX_RUNTIME)

def simulate_admit_candidate_to_sandbox_runtime_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.ADMIT_CANDIDATE_TO_SANDBOX_RUNTIME)

def simulate_start_sandbox_paper_session_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.START_SANDBOX_PAPER_SESSION)

def simulate_create_sandbox_paper_session_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.CREATE_SANDBOX_PAPER_SESSION)

def simulate_create_sandbox_paper_order_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.CREATE_SANDBOX_PAPER_ORDER)

def simulate_commit_sandbox_paper_state_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.COMMIT_SANDBOX_PAPER_STATE)

def simulate_patch_sandbox_runtime_config_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.PATCH_SANDBOX_RUNTIME_CONFIG)

def simulate_send_sandbox_broker_order_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.SEND_SANDBOX_BROKER_ORDER)

def simulate_send_sandbox_telegram_real_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.SEND_SANDBOX_TELEGRAM_REAL)

def simulate_unlock_sandbox_runtime_admission_gate_attempt(blocker: FinalPaperSandboxRuntimeAdmissionBlocker | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
    if not blocker: blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    return blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.UNLOCK_SANDBOX_RUNTIME_ADMISSION_GATE)

def sandbox_runtime_admission_attempt_simulator_summary(events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> dict[str, Any]:
    return {
        "total_simulated": len(events),
        "total_blocked": len([e for e in events if e.blocked])
    }

def sandbox_runtime_admission_attempt_simulator_to_text(events: list[PaperSandboxRuntimeAdmissionBlockerEvent], limit: int = 100) -> str:
    summary = sandbox_runtime_admission_attempt_simulator_summary(events)
    lines = [
        "--- Sandbox Runtime Admission Simulator ---",
        f"Simulated: {summary['total_simulated']}, Blocked: {summary['total_blocked']}"
    ]
    for e in events[:limit]:
        lines.append(f"  - {e.attempt_type.value}: Blocked={e.blocked}")
    return "\n".join(lines)
