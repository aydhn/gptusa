from typing import Any, List
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import SandboxRuntimeAdmissionReplayResult

def analyze_sandbox_runtime_admission_replay_result(result: SandboxRuntimeAdmissionReplayResult) -> dict[str, Any]:
    return {
        "passed": sandbox_runtime_admission_replay_passed(result),
        "requires_followup": sandbox_runtime_admission_replay_requires_followup(result),
        "followups": sandbox_runtime_admission_replay_followups(result),
        "risk_summary": sandbox_runtime_admission_replay_risk_summary(result)
    }

def sandbox_runtime_admission_replay_passed(result: SandboxRuntimeAdmissionReplayResult) -> bool:
    return result.passed and result.allowed_attempt_count == 0

def sandbox_runtime_admission_replay_requires_followup(result: SandboxRuntimeAdmissionReplayResult) -> bool:
    return not sandbox_runtime_admission_replay_passed(result)

def sandbox_runtime_admission_replay_followups(result: SandboxRuntimeAdmissionReplayResult) -> List[str]:
    followups = []
    if result.allowed_attempt_count > 0:
        followups.append("Fix admission attempts that were not blocked")
    if result.missing_event_count > 0:
        followups.append("Ensure all required attempts are recorded in sandbox events")
    return followups

def sandbox_runtime_admission_replay_risk_summary(result: SandboxRuntimeAdmissionReplayResult) -> dict[str, Any]:
    return {
        "risk_flag_count": len(result.risk_flags),
        "flags": [f.value for f in result.risk_flags]
    }

def sandbox_runtime_admission_replay_analyzer_to_text(payload: dict[str, Any]) -> str:
    res = f"Sandbox Replay Analysis:\nPassed: {payload.get('passed')}\n"
    if payload.get('requires_followup'):
        res += "Followups:\n"
        for f in payload.get('followups', []):
            res += f"- {f}\n"
    return res
