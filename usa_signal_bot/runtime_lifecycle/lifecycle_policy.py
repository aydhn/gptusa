from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import RuntimeLifecycleStatus

def build_phase104_lifecycle_policy() -> Dict[str, Any]:
    return {
        "metadata_only": True,
        "dry_run_only": True,
        "allow_activation": False,
        "allow_active_paper": False,
        "allow_broker_execution": False,
        "allow_paper_state_mutation": False,
        "allow_telegram_real_send": False,
        "allow_scraping": False,
        "allow_dashboard": False,
        "allowed_transitions": {
            RuntimeLifecycleStatus.DRAFT.value: [RuntimeLifecycleStatus.CREATED.value],
            RuntimeLifecycleStatus.CREATED.value: [RuntimeLifecycleStatus.CONFIG_CHECKED.value],
            RuntimeLifecycleStatus.CONFIG_CHECKED.value: [RuntimeLifecycleStatus.DEPENDENCIES_CHECKED.value],
            RuntimeLifecycleStatus.DEPENDENCIES_CHECKED.value: [RuntimeLifecycleStatus.READINESS_CHECKED.value],
            RuntimeLifecycleStatus.READINESS_CHECKED.value: [RuntimeLifecycleStatus.DRY_RUN_VALIDATED.value],
            RuntimeLifecycleStatus.DRY_RUN_VALIDATED.value: [RuntimeLifecycleStatus.READY_FOR_FUTURE_PHASE.value]
        }
    }

def validate_lifecycle_policy(policy: Dict[str, Any]) -> List[str]:
    errors = []
    if not policy.get("metadata_only", False):
        errors.append("Policy metadata_only MUST be True")
    if not policy.get("dry_run_only", False):
        errors.append("Policy dry_run_only MUST be True")
    if policy.get("allow_activation", False):
        errors.append("Policy allow_activation MUST be False")
    if policy.get("allow_active_paper", False):
        errors.append("Policy allow_active_paper MUST be False")
    if policy.get("allow_broker_execution", False):
        errors.append("Policy allow_broker_execution MUST be False")
    if policy.get("allow_paper_state_mutation", False):
        errors.append("Policy allow_paper_state_mutation MUST be False")
    if policy.get("allow_telegram_real_send", False):
        errors.append("Policy allow_telegram_real_send MUST be False")
    if policy.get("allow_scraping", False):
        errors.append("Policy allow_scraping MUST be False")
    if policy.get("allow_dashboard", False):
        errors.append("Policy allow_dashboard MUST be False")
    return errors

def lifecycle_policy_allows_transition(from_status: RuntimeLifecycleStatus, to_status: RuntimeLifecycleStatus, policy: Optional[Dict[str, Any]] = None) -> bool:
    if policy is None:
        policy = build_phase104_lifecycle_policy()

    allowed_dict = policy.get("allowed_transitions", {})
    allowed_targets = allowed_dict.get(from_status.value, [])

    if to_status.value in allowed_targets:
        return True

    # Always allow transitions to BLOCKED or FAILED or ARCHIVED for safety/abort
    if to_status in [RuntimeLifecycleStatus.BLOCKED, RuntimeLifecycleStatus.FAILED, RuntimeLifecycleStatus.ARCHIVED]:
        return True

    return False

def lifecycle_policy_blocks_execution(policy: Dict[str, Any]) -> bool:
    return len(validate_lifecycle_policy(policy)) == 0

def lifecycle_policy_to_text(policy: Dict[str, Any]) -> str:
    lines = ["=== LIFECYCLE POLICY ==="]
    for k, v in policy.items():
        if k == "allowed_transitions":
            lines.append("Allowed Transitions:")
            for from_st, to_sts in v.items():
                lines.append(f"  {from_st} -> {', '.join(to_sts)}")
        else:
            lines.append(f"{k}: {v}")
    return "\n".join(lines)
