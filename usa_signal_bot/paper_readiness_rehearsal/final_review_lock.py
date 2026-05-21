import datetime
import hashlib
import json
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import FinalReviewLockStatus, ReadinessRehearsalStatus
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    FinalReviewLock, ReadinessRehearsalRun, create_final_review_lock_id, validate_final_review_lock
)

def stable_final_lock_hash(payload: Dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

def lock_artifact_refs_from_run(run: ReadinessRehearsalRun) -> List[str]:
    refs = [run.run_id]
    if run.source_package_id:
        refs.append(run.source_package_id)
    if run.candidate_id:
        refs.append(run.candidate_id)
    return list(set(refs))

def build_final_review_lock(run: ReadinessRehearsalRun, package_payload: Optional[Dict[str, Any]] = None) -> FinalReviewLock:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if run.status != ReadinessRehearsalStatus.COMPLETED:
        status = FinalReviewLockStatus.LOCK_BLOCKED
        locked = False
        lock_reason = "Run not completed cleanly"
    else:
        status = FinalReviewLockStatus.LOCK_CREATED
        locked = True
        lock_reason = "Readiness Rehearsal successfully completed"

    hash_payload = {
        "run_id": run.run_id,
        "package_id": run.source_package_id,
        "candidate_id": run.candidate_id,
        "timestamp": now_utc
    }

    lock = FinalReviewLock(
        lock_id=create_final_review_lock_id(),
        created_at_utc=now_utc,
        status=status,
        source_rehearsal_run_id=run.run_id,
        source_package_id=run.source_package_id,
        candidate_id=run.candidate_id,
        locked=locked,
        lock_reason=lock_reason,
        lock_hash=stable_final_lock_hash(hash_payload),
        locked_artifact_refs=lock_artifact_refs_from_run(run),
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )
    validate_final_review_lock(lock)
    return lock

def final_review_lock_summary(lock: FinalReviewLock) -> Dict[str, Any]:
    return {
        "lock_id": lock.lock_id,
        "status": lock.status.value,
        "locked": lock.locked,
        "hash": lock.lock_hash
    }

def final_review_lock_to_text(lock: FinalReviewLock) -> str:
    return f"Final Review Lock: {lock.status.value} | Locked: {lock.locked} | Hash: {lock.lock_hash}"
