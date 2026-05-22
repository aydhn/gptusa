from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import RuntimeWriteLockProofRefresh
from usa_signal_bot.core.enums import WriteLockProofRefreshDecision

def validate_write_lock_refresh_safety(refresh: RuntimeWriteLockProofRefresh) -> List[str]:
    issues = []
    if not refresh.all_writes_blocked:
        issues.append("all_writes_blocked is False")
    if refresh.unblocked_write_attempt_count > 0:
        issues.append(f"unblocked_write_attempt_count is {refresh.unblocked_write_attempt_count}")
    if not refresh.hash_unchanged:
        issues.append("hash_unchanged is False")
    if refresh.mutation_detected:
        issues.append("mutation_detected is True")
    if refresh.allows_active_paper:
        issues.append("allows_active_paper is True")
    if refresh.allows_broker_execution:
        issues.append("allows_broker_execution is True")
    if refresh.allows_paper_state_mutation:
        issues.append("allows_paper_state_mutation is True")
    if refresh.allows_config_patch:
        issues.append("allows_config_patch is True")
    if refresh.allows_telegram_real_send:
        issues.append("allows_telegram_real_send is True")
    return issues

def write_lock_refresh_allows_activation(refresh: RuntimeWriteLockProofRefresh) -> bool:
    return any([
        refresh.allows_active_paper,
        refresh.allows_broker_execution,
        refresh.allows_paper_state_mutation,
        refresh.allows_config_patch,
        refresh.allows_telegram_real_send
    ])

def write_lock_refresh_requires_followup(refresh: RuntimeWriteLockProofRefresh) -> bool:
    return len(validate_write_lock_refresh_safety(refresh)) > 0 or write_lock_refresh_allows_activation(refresh)

def write_lock_refresh_blocks_dry_admission(refresh: RuntimeWriteLockProofRefresh) -> bool:
    return write_lock_refresh_requires_followup(refresh)

def write_lock_refresh_validator_summary(refresh: RuntimeWriteLockProofRefresh) -> dict[str, Any]:
    issues = validate_write_lock_refresh_safety(refresh)
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "blocks_dry_admission": write_lock_refresh_blocks_dry_admission(refresh)
    }

def write_lock_refresh_validator_to_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Valid: {payload.get('valid', False)}",
        f"Blocks Dry Admission: {payload.get('blocks_dry_admission', True)}"
    ]
    issues = payload.get("issues", [])
    if issues:
        lines.append("Issues:")
        for issue in issues:
            lines.append(f"  - {issue}")
    return "\n".join(lines)
