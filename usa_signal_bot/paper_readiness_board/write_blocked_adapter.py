
from typing import Any, List, Optional
import datetime
from usa_signal_bot.core.enums import RuntimeWriteAttemptType, WriteBlockAction, WriteBlockedAdapterStatus, PaperReadinessBoardRiskFlag
from usa_signal_bot.paper_readiness_board.readiness_board_models import RuntimeWriteBlockEvent, WriteBlockedRuntimeAdapterProof, create_runtime_write_block_event_id, create_write_block_proof_id

class WriteBlockedPaperRuntimeAdapter:
    def __init__(self, allow_reads: bool = True, block_writes: bool = True):
        self.allow_reads = allow_reads
        self.block_writes = block_writes

    def read_snapshot(self, paper_payload: dict = None) -> dict:
        if not self.allow_reads:
            return {}
        return dict(paper_payload or {})

    def attempt_write(self, attempt_type: RuntimeWriteAttemptType, payload: dict = None, source_component: str = None) -> RuntimeWriteBlockEvent:
        return RuntimeWriteBlockEvent(
            event_id=create_runtime_write_block_event_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            attempt_type=attempt_type,
            action=WriteBlockAction.DENY_AND_RECORD if self.block_writes else WriteBlockAction.UNKNOWN,
            blocked=self.block_writes,
            source_component=source_component,
            description=f"Attempt to write {attempt_type.value} blocked.",
            payload_summary={"payload_size": len(str(payload))} if payload else {},
            risk_flags=[], warnings=[], errors=[]
        )

    def attempt_paper_order_create(self, payload: dict = None) -> RuntimeWriteBlockEvent:
        return self.attempt_write(RuntimeWriteAttemptType.PAPER_ORDER_CREATE, payload)

    def attempt_paper_state_write(self, payload: dict = None) -> RuntimeWriteBlockEvent:
        return self.attempt_write(RuntimeWriteAttemptType.PAPER_STATE_WRITE, payload)

    def attempt_config_patch(self, payload: dict = None) -> RuntimeWriteBlockEvent:
        return self.attempt_write(RuntimeWriteAttemptType.CONFIG_PATCH, payload)

    def attempt_active_paper_enable(self, payload: dict = None) -> RuntimeWriteBlockEvent:
        return self.attempt_write(RuntimeWriteAttemptType.ACTIVE_PAPER_ENABLE, payload)

    def prove_all_writes_blocked(self, candidate_id: str = None) -> WriteBlockedRuntimeAdapterProof:
        # Generate dummy events
        events = [
            self.attempt_paper_order_create(),
            self.attempt_paper_state_write(),
            self.attempt_config_patch(),
            self.attempt_active_paper_enable()
        ]
        return build_write_deny_proof(events, candidate_id, "dummy_hash")

def required_write_attempt_types_for_proof() -> List[RuntimeWriteAttemptType]:
    return [
        RuntimeWriteAttemptType.PAPER_STATE_WRITE,
        RuntimeWriteAttemptType.PAPER_ORDER_CREATE,
        RuntimeWriteAttemptType.CONFIG_PATCH,
        RuntimeWriteAttemptType.ACTIVE_PAPER_ENABLE
    ]

def build_write_deny_proof(events: List[RuntimeWriteBlockEvent], candidate_id: str = None, snapshot_hash: str = None) -> WriteBlockedRuntimeAdapterProof:
    types_tested = list(set(e.attempt_type.value for e in events))
    blocked_count = sum(1 for e in events if e.blocked)
    unblocked_count = sum(1 for e in events if not e.blocked)
    all_blocked = unblocked_count == 0 and len(events) > 0

    return WriteBlockedRuntimeAdapterProof(
        proof_id=create_write_block_proof_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=WriteBlockedAdapterStatus.PROOF_CREATED if all_blocked else WriteBlockedAdapterStatus.FAILED,
        candidate_id=candidate_id,
        read_only_snapshot_hash=snapshot_hash,
        write_attempt_types_tested=types_tested,
        blocked_write_attempt_count=blocked_count,
        unblocked_write_attempt_count=unblocked_count,
        all_writes_blocked=all_blocked,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def proof_missing_attempt_types(proof: WriteBlockedRuntimeAdapterProof) -> List[str]:
    required = set(a.value for a in required_write_attempt_types_for_proof())
    tested = set(proof.write_attempt_types_tested)
    return list(required - tested)

def validate_write_deny_proof(proof: WriteBlockedRuntimeAdapterProof) -> List[str]:
    errors = []
    if not proof.all_writes_blocked:
        errors.append("Not all writes are blocked.")
    if proof.unblocked_write_attempt_count > 0:
        errors.append(f"Unblocked attempts found: {proof.unblocked_write_attempt_count}")
    return errors

def write_deny_proof_summary(proof: WriteBlockedRuntimeAdapterProof) -> dict:
    return {
        "status": proof.status.value,
        "all_writes_blocked": proof.all_writes_blocked,
        "blocked_count": proof.blocked_write_attempt_count
    }

def write_deny_proof_to_text(proof: WriteBlockedRuntimeAdapterProof) -> str:
    return f"Proof: {proof.status.value}, Blocked: {proof.blocked_write_attempt_count}, All Blocked: {proof.all_writes_blocked}"
