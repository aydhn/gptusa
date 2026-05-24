from typing import Any, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import BoardEvidenceFreezeBundle

def validate_board_evidence_freeze_bundle_safety(bundle: BoardEvidenceFreezeBundle) -> List[str]:
    errors = []
    if not bundle.frozen: errors.append("Bundle must be frozen")
    if not bundle.immutable: errors.append("Bundle must be immutable")
    if not bundle.freeze_is_metadata_only: errors.append("Bundle freeze_is_metadata_only must be True")
    if bundle.missing_evidence_count > 0: errors.append(f"Missing {bundle.missing_evidence_count} evidence items")
    if bundle.stale_evidence_count > 0: errors.append(f"Stale {bundle.stale_evidence_count} evidence items")
    return errors

def board_evidence_freeze_is_complete(bundle: BoardEvidenceFreezeBundle) -> bool:
    return bundle.missing_evidence_count == 0 and bundle.stale_evidence_count == 0

def board_evidence_freeze_requires_followup(bundle: BoardEvidenceFreezeBundle) -> bool:
    return not board_evidence_freeze_is_complete(bundle)

def board_evidence_freeze_blocks_next_stage(bundle: BoardEvidenceFreezeBundle) -> bool:
    return len(validate_board_evidence_freeze_bundle_safety(bundle)) > 0

def board_evidence_freeze_validator_summary(bundle: BoardEvidenceFreezeBundle) -> dict[str, Any]:
    return {
        "is_complete": board_evidence_freeze_is_complete(bundle),
        "requires_followup": board_evidence_freeze_requires_followup(bundle),
        "blocks_next_stage": board_evidence_freeze_blocks_next_stage(bundle),
        "errors": validate_board_evidence_freeze_bundle_safety(bundle)
    }

def board_evidence_freeze_validator_to_text(payload: dict[str, Any]) -> str:
    complete = payload.get("is_complete", False)
    blocks = payload.get("blocks_next_stage", True)
    return f"Board Evidence Validator - Complete: {complete}, Blocks Next Stage: {blocks}"
