from typing import Any, List
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import SimulatorEvidenceFreezeBundle

def validate_simulator_evidence_freeze_bundle_safety(bundle: SimulatorEvidenceFreezeBundle) -> List[str]:
    errors = []
    if not bundle.frozen:
        errors.append("Evidence bundle is not frozen")
    if not bundle.immutable:
        errors.append("Evidence bundle is not immutable")
    if not bundle.freeze_is_metadata_only:
        errors.append("Evidence bundle must be metadata-only")
    if bundle.missing_evidence_count > 0:
        errors.append(f"Bundle is missing {bundle.missing_evidence_count} evidence items")
    if bundle.stale_evidence_count > 0:
        errors.append(f"Bundle has {bundle.stale_evidence_count} stale evidence items")
    return errors

def simulator_evidence_freeze_is_complete(bundle: SimulatorEvidenceFreezeBundle) -> bool:
    return bundle.missing_evidence_count == 0 and bundle.stale_evidence_count == 0

def simulator_evidence_freeze_requires_followup(bundle: SimulatorEvidenceFreezeBundle) -> bool:
    return len(bundle.required_followups) > 0 or not simulator_evidence_freeze_is_complete(bundle)

def simulator_evidence_freeze_blocks_next_stage(bundle: SimulatorEvidenceFreezeBundle) -> bool:
    return simulator_evidence_freeze_requires_followup(bundle)

def simulator_evidence_freeze_validator_summary(bundle: SimulatorEvidenceFreezeBundle) -> dict[str, Any]:
    errors = validate_simulator_evidence_freeze_bundle_safety(bundle)
    return {
        "valid": len(errors) == 0,
        "complete": simulator_evidence_freeze_is_complete(bundle),
        "errors": errors
    }

def simulator_evidence_freeze_validator_to_text(payload: dict[str, Any]) -> str:
    res = f"Simulator Evidence Freeze Validation\nValid: {payload.get('valid')}\nComplete: {payload.get('complete')}\n"
    if payload.get("errors"):
        res += "Errors:\n"
        for e in payload.get("errors", []):
            res += f"- {e}\n"
    return res
