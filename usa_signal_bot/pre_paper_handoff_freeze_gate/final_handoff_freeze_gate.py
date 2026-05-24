import hashlib
import json
from datetime import datetime, timezone
from typing import Any, List, Optional
from usa_signal_bot.core.enums import (
    PrePaperHandoffFreezeGateStatus,
    PrePaperHandoffFreezeGateDecision,
    PrePaperHandoffFreezeRiskFlag
)
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    FinalPrePaperHandoffFreezeGate,
    HandoffFreezeRule,
    HandoffFreezeAssertion,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle,
    create_final_handoff_freeze_gate_id
)
from usa_signal_bot.core.serialization import serialize_value

def build_default_final_handoff_freeze_gate(candidate_id: Optional[str] = None) -> FinalPrePaperHandoffFreezeGate:
    return FinalPrePaperHandoffFreezeGate(
        gate_id=create_final_handoff_freeze_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=PrePaperHandoffFreezeGateStatus.DRAFT,
        decision=PrePaperHandoffFreezeGateDecision.UNKNOWN,
        candidate_id=candidate_id,
        source_simulator_dossier_review_id=None,
        source_simulator_dossier_id=None,
        source_simulator_acceptance_seal_id=None,
        source_sandbox_replay_result_id=None,
        source_simulator_evidence_freeze_id=None,
        sandbox_replay_result=None,
        evidence_freeze=None,
        rules=[],
        assertions=[],
        gate_hash=None,
        sealed=True,
        immutable=True,
        frozen=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        sandbox_runtime_admission_allowed=False,
        paper_sandbox_runtime_allowed=False,
        simulator_admission_allowed=False,
        local_paper_simulator_allowed=False,
        active_paper_enabled=False,
        pre_paper_handoff_complete=True,
        handoff_is_metadata_only=True,
        simulator_dossier_valid=True,
        simulator_acceptance_seal_valid=True,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def build_final_pre_paper_handoff_freeze_gate(payload: dict[str, Any]) -> FinalPrePaperHandoffFreezeGate:
    gate = build_default_final_handoff_freeze_gate(payload.get("candidate_id"))
    gate.source_simulator_dossier_review_id = payload.get("simulator_dossier_review_id")
    gate.source_simulator_dossier_id = payload.get("simulator_dossier_id")
    gate.source_simulator_acceptance_seal_id = payload.get("simulator_acceptance_seal_id")

    # Normally, the rules, assertions, replay result, and freeze bundle would be passed or extracted
    # The actual gate creation sets the hash
    gate.gate_hash = stable_handoff_freeze_gate_hash(serialize_value(gate))
    return gate

def stable_handoff_freeze_gate_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_handoff_freeze_gate_safety_flags(payload: dict[str, Any], rules: List[HandoffFreezeRule], assertions: List[HandoffFreezeAssertion]) -> List[PrePaperHandoffFreezeRiskFlag]:
    flags = []
    # Collect logic could examine rules/assertions statuses and add risk flags
    return flags

def final_handoff_freeze_gate_summary(gate: FinalPrePaperHandoffFreezeGate) -> dict[str, Any]:
    return {
        "gate_id": gate.gate_id,
        "status": gate.status.value,
        "decision": gate.decision.value,
        "pre_paper_handoff_complete": gate.pre_paper_handoff_complete
    }

def final_handoff_freeze_gate_to_text(gate: FinalPrePaperHandoffFreezeGate, limit: int = 100) -> str:
    return f"Final Handoff Freeze Gate: {gate.gate_id}\nStatus: {gate.status.value}\nComplete: {gate.pre_paper_handoff_complete}\n"
