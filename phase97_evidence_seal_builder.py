import os

path1 = "usa_signal_bot/paper_mode_dry_admission_dossier/dossier_evidence.py"
content1 = """from typing import Any
import datetime

from usa_signal_bot.core.enums import DryAdmissionDossierEvidenceStatus, DryAdmissionDossierRiskFlag
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionDossierEvidenceItem, create_dry_admission_dossier_evidence_id

def required_dry_admission_dossier_evidence_types() -> list[str]:
    return [
        "dry_admission_gate_full_review",
        "final_paper_mode_dry_admission_gate",
        "shadow_launch_replay_result",
        "board_evidence_freeze",
        "dry_admission_rules",
        "dry_admission_assertions",
        "dry_admission_continuity",
        "dry_admission_safety_report",
        "board_dossier_full_review",
        "acceptance_board_seal",
        "shadow_launch_blocker_events",
        "validation_reports",
        "audit_trails"
    ]

def evidence_item_from_dry_admission_source(
    evidence_type: str,
    source: Any | None,
    source_ref_id: str | None = None,
    source_path: str | None = None
) -> DryAdmissionDossierEvidenceItem:
    now = datetime.datetime.utcnow().isoformat() + "Z"

    available = source is not None
    status = DryAdmissionDossierEvidenceStatus.FRESH if available else DryAdmissionDossierEvidenceStatus.MISSING

    if available and isinstance(source, dict) and source.get("status") in ["STALE", "FAILED"]:
        status = DryAdmissionDossierEvidenceStatus.STALE if source.get("status") == "STALE" else DryAdmissionDossierEvidenceStatus.FAILED

    return DryAdmissionDossierEvidenceItem(
        evidence_id=create_dry_admission_dossier_evidence_id(),
        created_at_utc=now,
        evidence_type=evidence_type,
        source_ref_id=source_ref_id,
        source_path=source_path,
        status=status,
        required=evidence_type in required_dry_admission_dossier_evidence_types(),
        available=available,
        fresh=status == DryAdmissionDossierEvidenceStatus.FRESH,
        stale=status == DryAdmissionDossierEvidenceStatus.STALE,
        summary={"available": available, "type": evidence_type},
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={"source_extracted": True} if available else {}
    )

def collect_dry_admission_dossier_evidence(payload: dict[str, Any]) -> list[DryAdmissionDossierEvidenceItem]:
    items = []

    gate_review = payload.get("dry_admission_gate_full_review")
    items.append(evidence_item_from_dry_admission_source("dry_admission_gate_full_review", gate_review))

    final_gate = payload.get("final_dry_admission_gate")
    items.append(evidence_item_from_dry_admission_source("final_paper_mode_dry_admission_gate", final_gate))

    shadow_replay = payload.get("shadow_replay_result")
    items.append(evidence_item_from_dry_admission_source("shadow_launch_replay_result", shadow_replay))

    freeze = payload.get("board_evidence_freeze")
    items.append(evidence_item_from_dry_admission_source("board_evidence_freeze", freeze))

    rules = payload.get("dry_admission_rules")
    items.append(evidence_item_from_dry_admission_source("dry_admission_rules", rules))

    assertions = payload.get("dry_admission_assertions")
    items.append(evidence_item_from_dry_admission_source("dry_admission_assertions", assertions))

    # Add empty placeholders for other required types to ensure completeness
    other_types = [
        "dry_admission_continuity",
        "dry_admission_safety_report",
        "board_dossier_full_review",
        "acceptance_board_seal",
        "shadow_launch_blocker_events",
        "validation_reports",
        "audit_trails"
    ]

    for t in other_types:
        source = payload.get(t)
        items.append(evidence_item_from_dry_admission_source(t, source))

    return items

def dry_admission_evidence_missing_types(items: list[DryAdmissionDossierEvidenceItem]) -> list[str]:
    return [item.evidence_type for item in items if item.required and not item.available]

def dry_admission_evidence_stale_types(items: list[DryAdmissionDossierEvidenceItem]) -> list[str]:
    return [item.evidence_type for item in items if item.stale]

def dry_admission_evidence_score(items: list[DryAdmissionDossierEvidenceItem]) -> float | None:
    if not items:
        return 0.0

    required_items = [i for i in items if i.required]
    if not required_items:
        return 1.0

    available_required = [i for i in required_items if i.available and i.fresh]
    return len(available_required) / len(required_items)

def dry_admission_evidence_summary(items: list[DryAdmissionDossierEvidenceItem]) -> dict[str, Any]:
    return {
        "total": len(items),
        "available": sum(1 for i in items if i.available),
        "required_missing": len(dry_admission_evidence_missing_types(items)),
        "stale": len(dry_admission_evidence_stale_types(items)),
        "score": dry_admission_evidence_score(items)
    }

def dry_admission_dossier_evidence_to_text(items: list[DryAdmissionDossierEvidenceItem], limit: int = 100) -> str:
    summary = dry_admission_evidence_summary(items)
    text = f"Dry-Admission Dossier Evidence (Score: {summary['score']:.2f}):\n"
    text += f"- Total: {summary['total']}, Available: {summary['available']}\n"

    missing = dry_admission_evidence_missing_types(items)
    if missing:
        text += f"- Missing Required: {', '.join(missing[:limit])}\n"

    return text
"""

path2 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_acceptance_seal.py"
content2 = """from typing import Any
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
    text = f"Dry-Admission Acceptance Seal [{seal.seal_id}]:\n"
    text += f"- Status: {seal.status.value}\n"
    text += f"- Sealed/Immutable: {seal.sealed}/{seal.immutable}\n"
    return text
"""

path3 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_acceptance_seal_validator.py"
content3 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionAcceptanceSeal

def validate_dry_admission_acceptance_seal_safety(seal: DryAdmissionAcceptanceSeal) -> list[str]:
    errors = []
    if not seal.sealed:
        errors.append("Seal is not sealed")
    if not seal.immutable:
        errors.append("Seal is not immutable")
    if not seal.seal_is_metadata_only:
        errors.append("Seal is not metadata-only")
    if not seal.dry_admission_gate_passed:
        errors.append("Dry-admission gate not passed")
    if not seal.shadow_replay_passed:
        errors.append("Shadow replay not passed")
    if not seal.board_evidence_freeze_valid:
        errors.append("Board evidence freeze not valid")

    if not seal.no_rehearsal_confirmed:
        errors.append("No-rehearsal not confirmed")
    if not seal.no_order_confirmed:
        errors.append("No-order not confirmed")
    if not seal.no_write_confirmed:
        errors.append("No-write not confirmed")

    if seal.allows_rehearsal:
        errors.append("Seal allows rehearsal")
    if seal.allows_paper_mode_rehearsal:
        errors.append("Seal allows paper mode rehearsal")
    if seal.allows_shadow_launch:
        errors.append("Seal allows shadow launch")
    if seal.allows_paper_mode_launch:
        errors.append("Seal allows paper mode launch")
    if seal.allows_active_paper:
        errors.append("Seal allows active paper")
    if seal.allows_broker_execution:
        errors.append("Seal allows broker execution")
    if seal.allows_paper_state_mutation:
        errors.append("Seal allows paper state mutation")
    if seal.allows_config_patch:
        errors.append("Seal allows config patch")
    if seal.allows_telegram_real_send:
        errors.append("Seal allows telegram real send")

    return errors

def dry_admission_acceptance_seal_allows_rehearsal(seal: DryAdmissionAcceptanceSeal) -> bool:
    return seal.allows_rehearsal or seal.allows_paper_mode_rehearsal

def dry_admission_acceptance_seal_allows_execution(seal: DryAdmissionAcceptanceSeal) -> bool:
    return seal.allows_active_paper or seal.allows_broker_execution or seal.allows_paper_state_mutation

def dry_admission_acceptance_seal_requires_followup(seal: DryAdmissionAcceptanceSeal) -> bool:
    return len(seal.required_followups) > 0

def dry_admission_acceptance_seal_blocks_next_stage(seal: DryAdmissionAcceptanceSeal) -> bool:
    return len(validate_dry_admission_acceptance_seal_safety(seal)) > 0

def dry_admission_acceptance_seal_validator_summary(seal: DryAdmissionAcceptanceSeal) -> dict[str, Any]:
    errors = validate_dry_admission_acceptance_seal_safety(seal)
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def dry_admission_acceptance_seal_validator_to_text(payload: dict[str, Any]) -> str:
    valid = payload.get("valid", False)
    text = f"Seal Validator: {'PASS' if valid else 'FAIL'}\n"
    errors = payload.get("errors", [])
    if errors:
        text += f"- Errors: {', '.join(errors)}\n"
    return text
"""

with open(path1, "w") as f:
    f.write(content1)
with open(path2, "w") as f:
    f.write(content2)
with open(path3, "w") as f:
    f.write(content3)

print("Evidence and seal builder created")
