from typing import Any
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
    text = f"Seal Validator: {'PASS' if valid else 'FAIL'}
"
    errors = payload.get("errors", [])
    if errors:
        text += f"- Errors: {', '.join(errors)}
"
    return text
