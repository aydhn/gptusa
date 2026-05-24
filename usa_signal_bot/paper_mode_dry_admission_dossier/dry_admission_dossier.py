from typing import Any
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
    text = f"Dry-Admission Dossier [{dossier.dossier_id}]:
"
    text += f"- Status/Decision: {summary['status']} / {summary['decision']}
"
    text += f"- Sealed/Immutable: {summary['sealed']}/{summary['immutable']}
"
    text += f"- Evidence/Seal/Writes: {summary['evidence_count']}/{summary['seal_valid']}/{summary['all_writes_blocked']}
"
    return text
