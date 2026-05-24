from typing import Any
from usa_signal_bot.core.enums import ShadowLaunchAttemptType
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import ShadowLaunchBlockerEvent
from usa_signal_bot.paper_readiness_board_dossier.final_shadow_launch_blocker import FinalPaperModeShadowLaunchBlocker
from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_blocker_rules import dangerous_shadow_launch_attempt_types

def simulate_shadow_launch_attempts(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> list[ShadowLaunchBlockerEvent]:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    events = []

    # We explicitly call the specific simulation functions based on the requirements
    events.append(simulate_start_paper_mode_attempt(blocker))
    events.append(simulate_start_local_paper_runtime_attempt(blocker))
    events.append(simulate_shadow_launch_candidate_attempt(blocker))
    events.append(simulate_admit_candidate_to_paper_attempt(blocker))
    events.append(simulate_create_paper_session_attempt(blocker))
    events.append(simulate_create_paper_order_attempt(blocker))
    events.append(simulate_commit_paper_state_attempt(blocker))
    events.append(simulate_patch_paper_config_attempt(blocker))
    events.append(simulate_send_broker_order_attempt(blocker))
    events.append(simulate_send_telegram_real_attempt(blocker))
    events.append(simulate_unlock_shadow_launch_gate_attempt(blocker))

    return events

def simulate_start_paper_mode_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.START_PAPER_MODE, {"simulated": True}, "simulator")

def simulate_start_local_paper_runtime_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.START_LOCAL_PAPER_RUNTIME, {"simulated": True}, "simulator")

def simulate_shadow_launch_candidate_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.SHADOW_LAUNCH_CANDIDATE, {"simulated": True}, "simulator")

def simulate_admit_candidate_to_paper_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.ADMIT_CANDIDATE_TO_PAPER, {"simulated": True}, "simulator")

def simulate_create_paper_session_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.CREATE_PAPER_SESSION, {"simulated": True}, "simulator")

def simulate_create_paper_order_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.CREATE_PAPER_ORDER, {"simulated": True}, "simulator")

def simulate_commit_paper_state_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.COMMIT_PAPER_STATE, {"simulated": True}, "simulator")

def simulate_patch_paper_config_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.PATCH_PAPER_CONFIG, {"simulated": True}, "simulator")

def simulate_send_broker_order_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.SEND_BROKER_ORDER, {"simulated": True}, "simulator")

def simulate_send_telegram_real_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.SEND_TELEGRAM_REAL, {"simulated": True}, "simulator")

def simulate_unlock_shadow_launch_gate_attempt(blocker: FinalPaperModeShadowLaunchBlocker | None = None) -> ShadowLaunchBlockerEvent:
    blocker = blocker or FinalPaperModeShadowLaunchBlocker()
    return blocker.evaluate_attempt(ShadowLaunchAttemptType.UNLOCK_SHADOW_LAUNCH_GATE, {"simulated": True}, "simulator")

def shadow_launch_attempt_simulator_summary(events: list[ShadowLaunchBlockerEvent]) -> dict[str, Any]:
    return {
        "total_simulated_attempts": len(events),
        "total_blocked": sum(1 for e in events if e.blocked),
        "all_blocked": all(e.blocked for e in events),
        "covered_attempt_types": [e.attempt_type.name for e in events]
    }

def shadow_launch_attempt_simulator_to_text(events: list[ShadowLaunchBlockerEvent], limit: int = 100) -> str:
    lines = [f"Shadow Launch Simulator ({len(events)} events):"]
    for i, event in enumerate(events[:limit]):
        lines.append(f"  {i+1}. {event.attempt_type.name}: Blocked={event.blocked}")
    if len(events) > limit:
        lines.append(f"  ... and {len(events) - limit} more")
    return "\n".join(lines)
