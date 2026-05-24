from typing import Any, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import ShadowLaunchReplayResult
from usa_signal_bot.core.enums import ShadowLaunchReplayStatus, ShadowLaunchReplayOutcome

def analyze_shadow_replay_result(result: ShadowLaunchReplayResult) -> dict[str, Any]:
    return {
        "passed": shadow_replay_passed(result),
        "requires_followup": shadow_replay_requires_followup(result),
        "followups": shadow_replay_followups(result),
        "risk_summary": shadow_replay_risk_summary(result)
    }

def shadow_replay_passed(result: ShadowLaunchReplayResult) -> bool:
    return result.passed and result.status == ShadowLaunchReplayStatus.COMPLETED_ALL_BLOCKED and result.outcome == ShadowLaunchReplayOutcome.ALL_SHADOW_ATTEMPTS_BLOCKED and result.allowed_attempt_count == 0

def shadow_replay_requires_followup(result: ShadowLaunchReplayResult) -> bool:
    return not shadow_replay_passed(result)

def shadow_replay_followups(result: ShadowLaunchReplayResult) -> List[str]:
    followups = []
    if result.allowed_attempt_count > 0:
        followups.append("Investigate allowed shadow attempts")
    if result.missing_event_count > 0:
        followups.append("Provide missing shadow attempt events")
    if not result.passed:
        followups.append("Shadow replay must pass before dry-admission gate")
    return followups

def shadow_replay_risk_summary(result: ShadowLaunchReplayResult) -> dict[str, Any]:
    return {
        "flags": [f.value for f in result.risk_flags],
        "has_risks": len(result.risk_flags) > 0
    }

def shadow_replay_analyzer_to_text(payload: dict[str, Any]) -> str:
    passed = payload.get("passed", False)
    text = f"Shadow Replay Analyzer - Passed: {passed}\n"
    if payload.get("requires_followup"):
        text += "Followups:\n" + "\n".join(f"- {f}" for f in payload.get("followups", []))
    return text
