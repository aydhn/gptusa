import os

path1 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier.py"
content1 = """from typing import Any
import datetime
import hashlib
import json

from usa_signal_bot.core.enums import DryAdmissionDossierStatus, DryAdmissionDossierDecision, DryAdmissionDossierRiskFlag
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionGateDossier,
    DryAdmissionDossierEvidenceItem,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerEvent,
    create_dry_admission_dossier_id
)
from usa_signal_bot.paper_mode_dry_admission_dossier.dossier_evidence import collect_dry_admission_dossier_evidence
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_acceptance_seal import build_dry_admission_acceptance_seal
from usa_signal_bot.paper_mode_dry_admission_dossier.final_rehearsal_blocker import FinalPaperModeRehearsalBlocker
from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_attempt_simulator import simulate_rehearsal_attempts
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_gate_ingestion import (
    extract_final_dry_admission_gate,
    extract_shadow_replay_result,
    extract_board_evidence_freeze
)

def stable_dry_admission_dossier_hash(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def collect_dry_admission_dossier_safety_flags(payload: dict[str, Any], evidence_items: list[DryAdmissionDossierEvidenceItem]) -> list[DryAdmissionDossierRiskFlag]:
    flags = []

    # Check payload constraints
    if payload.get("activation_allowed"): flags.append(DryAdmissionDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed"): flags.append(DryAdmissionDossierRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed"): flags.append(DryAdmissionDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("shadow_launch_allowed"): flags.append(DryAdmissionDossierRiskFlag.SHADOW_LAUNCH_RISK)
    if payload.get("paper_mode_launch_allowed"): flags.append(DryAdmissionDossierRiskFlag.PAPER_MODE_LAUNCH_RISK)
    if payload.get("order_created"): flags.append(DryAdmissionDossierRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected"): flags.append(DryAdmissionDossierRiskFlag.MUTATION_DETECTED_RISK)

    # Check evidence constraints
    missing_required = any(e.required and not e.available for e in evidence_items)
    if missing_required:
        flags.append(DryAdmissionDossierRiskFlag.DOSSIER_EVIDENCE_MISSING)

    stale = any(e.stale for e in evidence_items)
    if stale:
        flags.append(DryAdmissionDossierRiskFlag.DOSSIER_EVIDENCE_STALE)

    return list(set(flags))

def build_default_dry_admission_dossier(candidate_id: str | None = None) -> DryAdmissionGateDossier:
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return DryAdmissionGateDossier(
        dossier_id=create_dry_admission_dossier_id(),
        created_at_utc=now,
        status=DryAdmissionDossierStatus.DRAFT,
        decision=DryAdmissionDossierDecision.UNKNOWN,
        candidate_id=candidate_id,
        source_dry_admission_review_id=None,
        source_dry_admission_gate_id=None,
        source_shadow_replay_result_id=None,
        source_board_evidence_freeze_id=None,
        evidence_items=[],
        acceptance_seal=None,
        rehearsal_blocker_events=[],
        evidence_refs=[],
        dossier_hash=None,
        sealed=False,
        immutable=False,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        shadow_launch_allowed=False,
        paper_mode_launch_allowed=False,
        rehearsal_allowed=False,
        paper_mode_rehearsal_allowed=False,
        dry_admission_gate_passed=False,
        board_dossier_valid=False,
        acceptance_seal_valid=False,
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
        errors=[],
        metadata={}
    )

def build_dry_admission_gate_dossier(payload: dict[str, Any]) -> DryAdmissionGateDossier:
    candidate_id = payload.get("candidate_id")
    dossier = build_default_dry_admission_dossier(candidate_id)

    # 1. Collect Evidence
    evidence_items = collect_dry_admission_dossier_evidence(payload)
    dossier.evidence_items = evidence_items
    dossier.evidence_refs = [e.evidence_id for e in evidence_items]

    # 2. Extract sources
    gate = extract_final_dry_admission_gate(payload)
    if gate:
        dossier.source_dry_admission_gate_id = gate.get("gate_id")
        dossier.dry_admission_gate_passed = gate.get("status") == "PASSED"

    replay = extract_shadow_replay_result(payload)
    if replay:
        dossier.source_shadow_replay_result_id = replay.get("replay_id")

    freeze = extract_board_evidence_freeze(payload)
    if freeze:
        dossier.source_board_evidence_freeze_id = freeze.get("freeze_id")

    # 3. Build Seal
    seal = build_dry_admission_acceptance_seal(payload, evidence_items)
    dossier.acceptance_seal = seal
    dossier.acceptance_seal_valid = seal.sealed and seal.immutable

    # 4. Rehearsal Blocker
    blocker = FinalPaperModeRehearsalBlocker()
    events = simulate_rehearsal_attempts(blocker)
    dossier.rehearsal_blocker_events = events
    dossier.all_writes_blocked = all(e.blocked for e in events)

    # 5. Evaluate Safety
    safety_flags = collect_dry_admission_dossier_safety_flags(payload, evidence_items)
    dossier.safety_flags = safety_flags

    if not safety_flags and dossier.dry_admission_gate_passed and dossier.acceptance_seal_valid and dossier.all_writes_blocked:
        dossier.status = DryAdmissionDossierStatus.VALIDATED_DRY_ADMISSION_SAFE
        dossier.decision = DryAdmissionDossierDecision.CREATE_DRY_ADMISSION_DOSSIER
        dossier.sealed = True
        dossier.immutable = True
    else:
        dossier.status = DryAdmissionDossierStatus.BLOCKED
        dossier.decision = DryAdmissionDossierDecision.BLOCK
        if safety_flags:
            dossier.required_followups.append("RESOLVE_SAFETY_FLAGS")
        if not dossier.dry_admission_gate_passed:
            dossier.required_followups.append("PASS_DRY_ADMISSION_GATE")
        if not dossier.acceptance_seal_valid:
            dossier.required_followups.append("OBTAIN_VALID_SEAL")

    dossier.dossier_hash = stable_dry_admission_dossier_hash(payload)

    return dossier

def dry_admission_dossier_summary(dossier: DryAdmissionGateDossier) -> dict[str, Any]:
    return {
        "dossier_id": dossier.dossier_id,
        "status": dossier.status.value,
        "decision": dossier.decision.value,
        "sealed": dossier.sealed,
        "immutable": dossier.immutable,
        "evidence_count": len(dossier.evidence_items),
        "seal_valid": dossier.acceptance_seal_valid,
        "all_writes_blocked": dossier.all_writes_blocked
    }

def dry_admission_dossier_to_text(dossier: DryAdmissionGateDossier, limit: int = 100) -> str:
    summary = dry_admission_dossier_summary(dossier)
    text = f"Dry-Admission Dossier [{dossier.dossier_id}]:\n"
    text += f"- Status/Decision: {summary['status']} / {summary['decision']}\n"
    text += f"- Sealed/Immutable: {summary['sealed']}/{summary['immutable']}\n"
    text += f"- Evidence/Seal/Writes: {summary['evidence_count']}/{summary['seal_valid']}/{summary['all_writes_blocked']}\n"
    return text
"""

path2 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier_continuity.py"
content2 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionGateDossier, DryAdmissionAcceptanceSeal, PaperModeRehearsalBlockerEvent
from usa_signal_bot.core.enums import DryAdmissionDossierRiskFlag

def validate_dry_admission_dossier_continuity(
    dossier: DryAdmissionGateDossier | None = None,
    seal: DryAdmissionAcceptanceSeal | None = None,
    blocker_events: list[PaperModeRehearsalBlockerEvent] | None = None
) -> list[str]:
    errors = []

    if dossier:
        if not dossier.activation_denied: errors.append("Dossier activation not denied")
        if dossier.activation_allowed: errors.append("Dossier allows activation")
        if dossier.admission_allowed: errors.append("Dossier allows admission")
        if dossier.transition_allowed: errors.append("Dossier allows transition")
        if dossier.shadow_launch_allowed: errors.append("Dossier allows shadow launch")
        if dossier.paper_mode_launch_allowed: errors.append("Dossier allows paper mode launch")
        if dossier.rehearsal_allowed: errors.append("Dossier allows rehearsal")
        if dossier.paper_mode_rehearsal_allowed: errors.append("Dossier allows paper mode rehearsal")
        if not dossier.all_writes_blocked: errors.append("Dossier writes not all blocked")
        if dossier.order_created: errors.append("Dossier order created")
        if dossier.mutation_detected: errors.append("Dossier mutation detected")
        if dossier.allows_active_paper: errors.append("Dossier allows active paper")
        if dossier.allows_broker_execution: errors.append("Dossier allows broker execution")

    if seal:
        if not seal.sealed or not seal.immutable: errors.append("Seal not valid")
        if seal.allows_rehearsal or seal.allows_paper_mode_rehearsal: errors.append("Seal allows rehearsal")

    if blocker_events:
        if any(not e.blocked for e in blocker_events): errors.append("Not all rehearsal attempts blocked")

    return errors

def dry_admission_dossier_continuity_flags(payload: dict[str, Any]) -> list[DryAdmissionDossierRiskFlag]:
    flags = []
    if payload.get("activation_allowed"): flags.append(DryAdmissionDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed"): flags.append(DryAdmissionDossierRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed"): flags.append(DryAdmissionDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    return flags

def dry_admission_dossier_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    flags = dry_admission_dossier_continuity_flags(payload)
    return len(flags) == 0

def dry_admission_dossier_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    flags = dry_admission_dossier_continuity_flags(payload)
    return {
        "preserved": len(flags) == 0,
        "flags": [f.value for f in flags]
    }

def dry_admission_dossier_continuity_to_text(payload: dict[str, Any]) -> str:
    summary = dry_admission_dossier_continuity_summary(payload)
    return f"Dossier Continuity: {'PRESERVED' if summary['preserved'] else 'BROKEN'}"
"""

path3 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier_safety_validator.py"
content3 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionGateDossier, DryAdmissionAcceptanceSeal, PaperModeRehearsalBlockerEvent
from usa_signal_bot.core.enums import DryAdmissionDossierRiskFlag

def collect_dry_admission_dossier_safety_flags(
    dossier: DryAdmissionGateDossier | None = None,
    seal: DryAdmissionAcceptanceSeal | None = None,
    blocker_events: list[PaperModeRehearsalBlockerEvent] | None = None
) -> list[DryAdmissionDossierRiskFlag]:
    flags = []

    if dossier:
        flags.extend(dossier.safety_flags)
        if dossier.activation_allowed: flags.append(DryAdmissionDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
        if dossier.allows_broker_execution: flags.append(DryAdmissionDossierRiskFlag.BROKER_ORDER_RISK)
        if dossier.allows_paper_state_mutation: flags.append(DryAdmissionDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
        if dossier.allows_telegram_real_send: flags.append(DryAdmissionDossierRiskFlag.TELEGRAM_REAL_SEND_RISK)

    if seal:
        if seal.allows_active_paper: flags.append(DryAdmissionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if seal.allows_rehearsal: flags.append(DryAdmissionDossierRiskFlag.PAPER_MODE_REHEARSAL_RISK)

    if blocker_events:
        if any(not e.blocked for e in blocker_events):
            flags.append(DryAdmissionDossierRiskFlag.REHEARSAL_ATTEMPT_NOT_BLOCKED)

    return list(set(flags))

def dry_admission_dossier_has_blocking_flags(flags: list[DryAdmissionDossierRiskFlag]) -> bool:
    return len(flags) > 0

def validate_dry_admission_dossier_safety(
    dossier: DryAdmissionGateDossier | None = None,
    seal: DryAdmissionAcceptanceSeal | None = None,
    blocker_events: list[PaperModeRehearsalBlockerEvent] | None = None
) -> list[str]:
    flags = collect_dry_admission_dossier_safety_flags(dossier, seal, blocker_events)
    return [f.value for f in flags]

def dry_admission_dossier_safety_summary(flags: list[DryAdmissionDossierRiskFlag]) -> dict[str, Any]:
    return {
        "safe": len(flags) == 0,
        "flags": [f.value for f in flags]
    }

def dry_admission_dossier_safety_validator_to_text(payload: dict[str, Any]) -> str:
    safe = payload.get("safe", False)
    return f"Dossier Safety: {'SAFE' if safe else 'UNSAFE'}"
"""

with open(path1, "w") as f:
    f.write(content1)
with open(path2, "w") as f:
    f.write(content2)
with open(path3, "w") as f:
    f.write(content3)

print("Dossier and safety validator created")
