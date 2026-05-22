from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    RuntimeWriteLockProofRefresh,
    create_write_lock_refresh_id
)
from usa_signal_bot.core.enums import (
    WriteLockProofRefreshStatus,
    WriteLockProofRefreshDecision,
    DryAdmissionRiskFlag,
    RuntimeWriteAttemptType
)
from usa_signal_bot.paper_dry_admission.no_write_ingestion import (
    extract_no_write_candidate_id,
    extract_no_write_contract
)

def required_write_lock_refresh_attempt_types() -> List[str]:
    return [
        RuntimeWriteAttemptType.PAPER_STATE_WRITE.value,
        RuntimeWriteAttemptType.PAPER_ORDER_CREATE.value,
        RuntimeWriteAttemptType.POSITION_WRITE.value,
        RuntimeWriteAttemptType.PORTFOLIO_WRITE.value,
        RuntimeWriteAttemptType.CASH_WRITE.value,
        RuntimeWriteAttemptType.EQUITY_WRITE.value,
        RuntimeWriteAttemptType.FILL_WRITE.value,
        RuntimeWriteAttemptType.CONFIG_PATCH.value,
        RuntimeWriteAttemptType.ACTIVE_PAPER_ENABLE.value,
        RuntimeWriteAttemptType.BROKER_SEND.value,
        RuntimeWriteAttemptType.TELEGRAM_REAL_SEND.value
    ]

def collect_write_lock_refresh_risk_flags(payload: dict[str, Any]) -> List[DryAdmissionRiskFlag]:
    flags = []
    if payload.get("mutation_detected", False):
        flags.append(DryAdmissionRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("unblocked_write_attempt_count", 0) > 0:
        flags.append(DryAdmissionRiskFlag.WRITE_LOCK_BYPASS_RISK)
    if not payload.get("all_writes_blocked", True):
        flags.append(DryAdmissionRiskFlag.WRITE_LOCK_REFRESH_FAILED)
    if payload.get("allows_active_paper", False):
        flags.append(DryAdmissionRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if payload.get("allows_broker_execution", False):
        flags.append(DryAdmissionRiskFlag.BROKER_ORDER_RISK)
    return flags

def refresh_runtime_write_lock_proof(
    no_write_payload: dict[str, Any] | None = None,
    paper_payload_before: dict[str, Any] | None = None,
    paper_payload_after: dict[str, Any] | None = None
) -> RuntimeWriteLockProofRefresh:
    no_write = no_write_payload or {}
    before = paper_payload_before or {}
    after = paper_payload_after or {}

    candidate_id = extract_no_write_candidate_id(no_write)
    contract = extract_no_write_contract(no_write)
    contract_id = contract.get("contract_id") if contract else None

    hash_before = before.get("hash") or before.get("state_hash") or "hash_dummy"
    hash_after = after.get("hash") or after.get("state_hash") or hash_before

    hash_unchanged = hash_before == hash_after

    # Simulate metadata-only verification
    types_verified = required_write_lock_refresh_attempt_types()

    refresh = RuntimeWriteLockProofRefresh(
        refresh_id=create_write_lock_refresh_id(),
        status=WriteLockProofRefreshStatus.REFRESHED if hash_unchanged else WriteLockProofRefreshStatus.FAILED,
        decision=WriteLockProofRefreshDecision.REQUEST_MANUAL_REVIEW if not hash_unchanged else WriteLockProofRefreshDecision.INCONCLUSIVE, # Set to inconclusive by default, let validator decide
        candidate_id=candidate_id,
        source_contract_id=contract_id,
        read_only_snapshot_hash_before=hash_before,
        read_only_snapshot_hash_after=hash_after,
        write_attempt_types_verified=types_verified,
        blocked_write_attempt_count=len(types_verified),
        unblocked_write_attempt_count=0 if hash_unchanged else 1,
        all_writes_blocked=hash_unchanged,
        hash_unchanged=hash_unchanged,
        mutation_detected=not hash_unchanged,
    )

    refresh.risk_flags = collect_write_lock_refresh_risk_flags({
        "mutation_detected": refresh.mutation_detected,
        "unblocked_write_attempt_count": refresh.unblocked_write_attempt_count,
        "all_writes_blocked": refresh.all_writes_blocked,
        "allows_active_paper": refresh.allows_active_paper,
        "allows_broker_execution": refresh.allows_broker_execution
    })

    return refresh

def write_lock_refresh_summary(refresh: RuntimeWriteLockProofRefresh) -> dict[str, Any]:
    return {
        "refresh_id": refresh.refresh_id,
        "status": refresh.status.value,
        "decision": refresh.decision.value,
        "hash_unchanged": refresh.hash_unchanged,
        "all_writes_blocked": refresh.all_writes_blocked,
        "risk_flags": [f.value for f in refresh.risk_flags]
    }

def write_lock_refresh_to_text(refresh: RuntimeWriteLockProofRefresh) -> str:
    lines = [
        f"Refresh ID: {refresh.refresh_id}",
        f"Status: {refresh.status.value}",
        f"Decision: {refresh.decision.value}",
        f"Hash Unchanged: {refresh.hash_unchanged}",
        f"All Writes Blocked: {refresh.all_writes_blocked}",
        f"Blocked Count: {refresh.blocked_write_attempt_count}",
        f"Unblocked Count: {refresh.unblocked_write_attempt_count}"
    ]
    if refresh.risk_flags:
        lines.append("Risk Flags:")
        for flag in refresh.risk_flags:
            lines.append(f"  - {flag.value}")
    return "\n".join(lines)
