from typing import Any
from .simulator_gate_models import RehearsalReplayResult

def analyze_rehearsal_replay_result(result: RehearsalReplayResult) -> dict[str, Any]:
    return {}

def rehearsal_replay_passed(result: RehearsalReplayResult) -> bool:
    if result.allowed_attempt_count > 0:
        return False
    return result.passed

def rehearsal_replay_requires_followup(result: RehearsalReplayResult) -> bool:
    return False

def rehearsal_replay_followups(result: RehearsalReplayResult) -> list[str]:
    return []

def rehearsal_replay_risk_summary(result: RehearsalReplayResult) -> dict[str, Any]:
    return {}

def rehearsal_replay_analyzer_to_text(payload: dict[str, Any]) -> str:
    return ""
