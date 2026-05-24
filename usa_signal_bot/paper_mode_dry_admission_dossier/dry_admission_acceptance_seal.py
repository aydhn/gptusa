from typing import Any
import datetime
import hashlib
import json

from usa_signal_bot.core.enums import DryAdmissionAcceptanceSealStatus, DryAdmissionAcceptanceSealDecision, DryAdmissionDossierRiskFlag
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionAcceptanceSeal, DryAdmissionDossierEvidenceItem, create_dry_admission_acceptance_seal_id
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_gate_ingestion import extract_final_dry_admission_gate, extract_shadow_replay_result, extract_board_evidence_freeze

def accepted_dry_admission_boundaries() -> list[str]:
    return [
        "dry_admission_gate_passed",
        "shadow_replay_passed",
        "board_evidence_freeze_valid",
        "no_shadow_launch_permission",
        "no_paper_mode_launch_permission",
        "no_rehearsal_permission",
        "no_paper_admission_permission",
        "no_order_creation",
        "no_paper_state_write",
        "no_broker_execution",
        "no_config_patch",
        "no_telegram_real_send",
        "not_investment_advice"
    ]

def stable_dry_admission_acceptance_seal_hash(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def collect_dry_admission_acceptance_seal_risk_flags(payload: dict[str, Any]) -> list[DryAdmissionDossierRiskFlag]:
    flags = []
    if payload.get("allows_rehearsal") is True:
        flags.append(DryAdmissionDossierRiskFlag.PAPER_MODE_REHEARSAL_RISK)
    if payload.get("allows_active_paper") is True:
        flags.append(DryAdmissionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    return flags

def build_default_dry_admission_acceptance_seal(candidate_id: str | None = None) -> DryAdmissionAcceptanceSeal:
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return DryAdmissionAcceptanceSeal(
        seal_id=create_dry_admission_acceptance_seal_id(),
        created_at_utc=now,
        status=DryAdmissionAcceptanceSealStatus.DRAFT,
        decision=DryAdmissionAcceptanceSealDecision.UNKNOWN,
        candidate_id=candidate_id,
        source_dry_admission_gate_id=None,
        source_dry_admission_review_id=None,
        source_shadow_replay_result_id=None,
        source_board_evidence_freeze_id=None,
        seal_hash=None,
        accepted_boundaries=accepted_dry_admission_boundaries(),
        dry_admission_gate_passed=False,
        shadow_replay_passed=False,
        board_evidence_freeze_valid=False,
        dry_admission_rules_passed=False,
        dry_admission_assertions_passed=False,
        no_shadow_launch_confirmed=True,
        no_paper_mode_launch_confirmed=True,
        no_rehearsal_confirmed=True,
        no_admission_confirmed=True,
        no_order_confirmed=True,
        no_write_confirmed=True,
        no_broker_confirmed=True,
        no_config_patch_confirmed=True,
        no_telegram_real_send_confirmed=True,
        sealed=False,
        immutable=False,
        seal_is_metadata_only=True,
        allows_rehearsal=False,
        allows_paper_mode_rehearsal=False,
        allows_shadow_launch=False,
        allows_paper_mode_launch=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_dry_admission_acceptance_seal(
    payload: dict[str, Any],
    evidence_items: list[DryAdmissionDossierEvidenceItem] | None = None
) -> DryAdmissionAcceptanceSeal:
    seal = build_default_dry_admission_acceptance_seal(payload.get("candidate_id"))

    gate = extract_final_dry_admission_gate(payload)
    if gate and gate.get("status") == "PASSED":
        seal.dry_admission_gate_passed = True
        seal.source_dry_admission_gate_id = gate.get("gate_id")

    replay = extract_shadow_replay_result(payload)
    if replay and replay.get("status") == "PASSED":
        seal.shadow_replay_passed = True
        seal.source_shadow_replay_result_id = replay.get("replay_id")

    freeze = extract_board_evidence_freeze(payload)
    if freeze and freeze.get("status") == "VALID":
        seal.board_evidence_freeze_valid = True
        seal.source_board_evidence_freeze_id = freeze.get("freeze_id")

    if seal.dry_admission_gate_passed and seal.shadow_replay_passed and seal.board_evidence_freeze_valid:
        seal.status = DryAdmissionAcceptanceSealStatus.SEALED
        seal.decision = DryAdmissionAcceptanceSealDecision.SEAL_DRY_ADMISSION_ACCEPTANCE
        seal.sealed = True
        seal.immutable = True
    else:
        seal.status = DryAdmissionAcceptanceSealStatus.FAILED
        seal.decision = DryAdmissionAcceptanceSealDecision.BLOCK

    seal.seal_hash = stable_dry_admission_acceptance_seal_hash(payload)
    return seal

def dry_admission_acceptance_seal_summary(seal: DryAdmissionAcceptanceSeal) -> dict[str, Any]:
    return {
        "seal_id": seal.seal_id,
        "status": seal.status.value,
        "sealed": seal.sealed,
        "immutable": seal.immutable,
        "all_writes_blocked": True
    }

def dry_admission_acceptance_seal_to_text(seal: DryAdmissionAcceptanceSeal) -> str:
    text = f"Dry-Admission Acceptance Seal [{seal.seal_id}]:
"
    text += f"- Status: {seal.status.value}
"
    text += f"- Sealed/Immutable: {seal.sealed}/{seal.immutable}
"
    return text
