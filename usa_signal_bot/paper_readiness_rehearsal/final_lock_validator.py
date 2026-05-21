from typing import Any, Dict, List
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import FinalReviewLock
from usa_signal_bot.core.enums import FinalReviewLockStatus

def validate_final_lock_safety(lock: FinalReviewLock) -> List[str]:
    errors = []
    if lock.allows_active_paper:
        errors.append("Lock unexpectedly allows active paper")
    if lock.allows_broker_execution:
        errors.append("Lock unexpectedly allows broker execution")
    if lock.allows_paper_state_mutation:
        errors.append("Lock unexpectedly allows paper state mutation")
    if lock.allows_config_patch:
        errors.append("Lock unexpectedly allows config patch")
    return errors

def validate_final_lock_artifacts(lock: FinalReviewLock) -> List[str]:
    errors = []
    if not lock.locked_artifact_refs:
        errors.append("Missing artifact refs in lock")
    return errors

def final_lock_allows_activation(lock: FinalReviewLock) -> bool:
    # Final lock is metadata only, NEVER allows activation
    return False

def final_lock_blocks_handoff(lock: FinalReviewLock) -> bool:
    if not lock.locked:
        return True
    if lock.status in [FinalReviewLockStatus.LOCK_BLOCKED, FinalReviewLockStatus.LOCK_EXPIRED, FinalReviewLockStatus.DRAFT]:
        return True
    if validate_final_lock_safety(lock) or validate_final_lock_artifacts(lock):
        return True
    return False

def final_lock_validator_summary(lock: FinalReviewLock) -> Dict[str, Any]:
    return {
        "is_safe": not bool(validate_final_lock_safety(lock)),
        "blocks_handoff": final_lock_blocks_handoff(lock)
    }

def final_lock_validator_to_text(payload: Dict[str, Any]) -> str:
    return f"Lock Validator: safe={payload.get('is_safe', False)}, blocks_handoff={payload.get('blocks_handoff', True)}"
