from typing import Any, Optional
import datetime
import hashlib
import json
from usa_signal_bot.core.enums import PaperSandboxBridgeStatus, PaperSandboxBridgeDecision
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    PaperSandboxBridgeEnvelope,
    create_bridge_envelope_id
)
from usa_signal_bot.paper_no_write_transition.sandbox_bridge_route_map import default_sandbox_bridge_routes

def paper_sandbox_bridge_snapshot_hash(paper_snapshot: Optional[dict[str, Any]] = None) -> str:
    if not paper_snapshot:
        return "empty"
    s = json.dumps(paper_snapshot, sort_keys=True)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def build_paper_sandbox_bridge_envelope(
    dossier_id: Optional[str] = None,
    candidate_id: Optional[str] = None,
    transition_checkpoint_id: Optional[str] = None,
    evidence_seal_id: Optional[str] = None,
    paper_snapshot: Optional[dict[str, Any]] = None
) -> PaperSandboxBridgeEnvelope:

    return PaperSandboxBridgeEnvelope(
        bridge_id=create_bridge_envelope_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=PaperSandboxBridgeStatus.VALIDATED_NO_WRITE,
        decision=PaperSandboxBridgeDecision.CREATE_NO_WRITE_SANDBOX_BRIDGE,
        candidate_id=candidate_id,
        source_dossier_id=dossier_id,
        source_transition_checkpoint_id=transition_checkpoint_id,
        source_evidence_seal_id=evidence_seal_id,
        routes=default_sandbox_bridge_routes(),
        read_only_snapshot_hash=paper_sandbox_bridge_snapshot_hash(paper_snapshot),
        bridge_is_no_write=True,
        bridge_is_metadata_only=True,
        activation_denied=True,
        activation_allowed=False,
        transition_allowed=False,
        all_writes_blocked=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def build_default_paper_sandbox_bridge_envelope(candidate_id: Optional[str] = None) -> PaperSandboxBridgeEnvelope:
    return build_paper_sandbox_bridge_envelope(candidate_id=candidate_id)

def validate_paper_sandbox_bridge_envelope_safety(envelope: PaperSandboxBridgeEnvelope) -> list[str]:
    from usa_signal_bot.paper_no_write_transition.bridge_route_guard import validate_all_bridge_routes_no_write
    errors = validate_all_bridge_routes_no_write(envelope.routes)
    if not envelope.bridge_is_no_write:
        errors.append("Envelope is not no-write.")
    if not envelope.bridge_is_metadata_only:
        errors.append("Envelope is not metadata-only.")
    if envelope.activation_allowed:
        errors.append("Activation is allowed.")
    return errors

def paper_sandbox_bridge_envelope_summary(envelope: PaperSandboxBridgeEnvelope) -> dict[str, Any]:
    return {
        "bridge_id": envelope.bridge_id,
        "status": envelope.status.value,
        "is_no_write": envelope.bridge_is_no_write,
        "activation_denied": envelope.activation_denied
    }

def paper_sandbox_bridge_envelope_to_text(envelope: PaperSandboxBridgeEnvelope, limit: int = 100) -> str:
    return f"Sandbox Bridge Envelope [{envelope.status.value}] No-write: {envelope.bridge_is_no_write} Activation Denied: {envelope.activation_denied}"
