from typing import Any
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import AdmissionBlockerReplayResult

def analyze_blocker_replay_result(result: AdmissionBlockerReplayResult) -> dict[str, Any]:
    return {"passed": result.passed, "followups": blocker_replay_followups(result)}

def blocker_replay_passed(result: AdmissionBlockerReplayResult) -> bool:
    return result.passed

def blocker_replay_requires_followup(result: AdmissionBlockerReplayResult) -> bool:
    return not result.passed

def blocker_replay_followups(result: AdmissionBlockerReplayResult) -> list[str]:
    if not result.passed:
        return ["Replay failed, manual review required", "Check blocker rules"]
    return []

def blocker_replay_risk_summary(result: AdmissionBlockerReplayResult) -> dict[str, Any]:
    return {"risk_flags": [f.value for f in result.risk_flags]}

def blocker_replay_analyzer_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
