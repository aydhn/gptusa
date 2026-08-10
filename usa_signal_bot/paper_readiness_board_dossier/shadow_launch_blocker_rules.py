from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    ShadowLaunchAttemptType,
    ShadowLaunchBlockerAction,
    BoardDossierRiskFlag
)
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    ShadowLaunchBlockerRule,
    create_shadow_launch_blocker_rule_id
)

def dangerous_shadow_launch_attempt_types() -> list[ShadowLaunchAttemptType]:
    return [
        ShadowLaunchAttemptType.START_PAPER_MODE,
        ShadowLaunchAttemptType.START_LOCAL_PAPER_RUNTIME,
        ShadowLaunchAttemptType.SHADOW_LAUNCH_CANDIDATE,
        ShadowLaunchAttemptType.ADMIT_CANDIDATE_TO_PAPER,
        ShadowLaunchAttemptType.CREATE_PAPER_SESSION,
        ShadowLaunchAttemptType.CREATE_PAPER_ORDER,
        ShadowLaunchAttemptType.COMMIT_PAPER_STATE,
        ShadowLaunchAttemptType.PATCH_PAPER_CONFIG,
        ShadowLaunchAttemptType.SEND_BROKER_ORDER,
        ShadowLaunchAttemptType.SEND_TELEGRAM_REAL,
        ShadowLaunchAttemptType.UNLOCK_SHADOW_LAUNCH_GATE
    ]

def rule_for_shadow_launch_attempt(attempt_type: ShadowLaunchAttemptType) -> ShadowLaunchBlockerRule:
    risk_mapping = {
        ShadowLaunchAttemptType.START_PAPER_MODE: BoardDossierRiskFlag.PAPER_MODE_LAUNCH_RISK,
        ShadowLaunchAttemptType.START_LOCAL_PAPER_RUNTIME: BoardDossierRiskFlag.PAPER_MODE_LAUNCH_RISK,
        ShadowLaunchAttemptType.SHADOW_LAUNCH_CANDIDATE: BoardDossierRiskFlag.SHADOW_LAUNCH_RISK,
        ShadowLaunchAttemptType.ADMIT_CANDIDATE_TO_PAPER: BoardDossierRiskFlag.PAPER_ADMISSION_RISK,
        ShadowLaunchAttemptType.CREATE_PAPER_SESSION: BoardDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        ShadowLaunchAttemptType.CREATE_PAPER_ORDER: BoardDossierRiskFlag.PAPER_ORDER_RISK,
        ShadowLaunchAttemptType.COMMIT_PAPER_STATE: BoardDossierRiskFlag.PAPER_STATE_MUTATION_RISK,
        ShadowLaunchAttemptType.PATCH_PAPER_CONFIG: BoardDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        ShadowLaunchAttemptType.SEND_BROKER_ORDER: BoardDossierRiskFlag.BROKER_ORDER_RISK,
        ShadowLaunchAttemptType.SEND_TELEGRAM_REAL: BoardDossierRiskFlag.TELEGRAM_REAL_SEND_RISK,
        ShadowLaunchAttemptType.UNLOCK_SHADOW_LAUNCH_GATE: BoardDossierRiskFlag.SHADOW_LAUNCH_RISK
    }

    return ShadowLaunchBlockerRule(
        rule_id=create_shadow_launch_blocker_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        attempt_type=attempt_type,
        enabled=True,
        blocking=True,
        action=ShadowLaunchBlockerAction.DENY_AND_RECORD,
        description=f"Block {attempt_type.name} attempt unconditionally during non-execution phase",
        risk_flags=[risk_mapping.get(attempt_type, BoardDossierRiskFlag.UNKNOWN)],
        warnings=[],
        errors=[]
    )

def default_shadow_launch_blocker_rules() -> list[ShadowLaunchBlockerRule]:
    return [rule_for_shadow_launch_attempt(at) for at in dangerous_shadow_launch_attempt_types()]

def validate_shadow_launch_blocker_rules_complete(rules: list[ShadowLaunchBlockerRule]) -> list[str]:
    issues = []
    action_deny = ShadowLaunchBlockerAction.DENY
    action_deny_and_record = ShadowLaunchBlockerAction.DENY_AND_RECORD
    covered_types = {r.attempt_type for r in rules if r.enabled and r.blocking and (r.action is action_deny or r.action is action_deny_and_record)}

    for required in dangerous_shadow_launch_attempt_types():
        if required not in covered_types:
            issues.append(f"Missing active blocking rule for {required.name}")

    return issues

def shadow_launch_blocker_rules_summary(rules: list[ShadowLaunchBlockerRule]) -> dict[str, Any]:
    issues = validate_shadow_launch_blocker_rules_complete(rules)
    return {
        "total_rules": len(rules),
        "active_blocking_rules": sum(1 for r in rules if r.enabled and r.blocking),
        "is_complete": len(issues) == 0,
        "missing_coverage_count": len(issues)
    }

def shadow_launch_blocker_rules_to_text(rules: list[ShadowLaunchBlockerRule], limit: int = 100) -> str:
    lines = [f"Shadow Launch Blocker Rules ({len(rules)} items):"]
    for i, rule in enumerate(rules[:limit]):
        lines.append(f"  {i+1}. {rule.attempt_type.name}: {rule.action.name} (Enabled: {rule.enabled}, Blocking: {rule.blocking})")
    if len(rules) > limit:
        lines.append(f"  ... and {len(rules) - limit} more")
    return "\n".join(lines)
