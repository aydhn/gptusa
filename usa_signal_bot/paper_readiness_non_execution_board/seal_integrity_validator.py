from typing import Any, Dict, List
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import NonExecutionSealIntegrityAudit

def validate_non_execution_seal_integrity_audit(audit: NonExecutionSealIntegrityAudit) -> List[str]:
    errors = []
    if not audit.seal_hash_matches:
        errors.append("Seal hash mismatch")
    if audit.failed_item_count > 0:
        errors.append(f"{audit.failed_item_count} confirmation items failed")
    if audit.missing_boundary_count > 0:
        errors.append(f"{audit.missing_boundary_count} boundaries missing")
    if not audit.confirmed_non_execution:
        errors.append("Non-execution not confirmed")
    if not audit.seal_is_metadata_only:
        errors.append("Seal is not metadata only")
    if not audit.integrity_valid and len(errors) == 0:
        errors.append("Integrity is marked invalid for unknown reasons")
    return errors

def non_execution_seal_integrity_is_valid(audit: NonExecutionSealIntegrityAudit) -> bool:
    return audit.integrity_valid and len(validate_non_execution_seal_integrity_audit(audit)) == 0

def non_execution_seal_integrity_requires_followup(audit: NonExecutionSealIntegrityAudit) -> bool:
    return not non_execution_seal_integrity_is_valid(audit)

def non_execution_seal_integrity_blocks_next_stage(audit: NonExecutionSealIntegrityAudit) -> bool:
    # Any failure in seal integrity blocks the final board
    return not audit.integrity_valid

def seal_integrity_validator_summary(audit: NonExecutionSealIntegrityAudit) -> Dict[str, Any]:
    return {
        "valid": non_execution_seal_integrity_is_valid(audit),
        "errors": validate_non_execution_seal_integrity_audit(audit)
    }

def seal_integrity_validator_to_text(payload: Dict[str, Any]) -> str:
    lines = ["--- SEAL INTEGRITY VALIDATOR ---"]
    lines.append(f"Valid: {payload.get('valid')}")
    if payload.get("errors"):
        lines.append("Errors:")
        for e in payload.get("errors"):
            lines.append(f"  - {e}")
    return "\n".join(lines)
