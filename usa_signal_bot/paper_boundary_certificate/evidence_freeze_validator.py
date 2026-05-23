from typing import Any
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import NoOrderEvidenceFreezeBundle

def validate_evidence_freeze_bundle_safety(bundle: NoOrderEvidenceFreezeBundle) -> list[str]:
    errors = []
    if not bundle.frozen:
        errors.append("Evidence freeze is not frozen")
    if not bundle.immutable:
        errors.append("Evidence freeze is not immutable")
    if not bundle.freeze_is_metadata_only:
        errors.append("Evidence freeze is not metadata only")
    if bundle.missing_evidence_count > 0:
        errors.append(f"Missing evidence count: {bundle.missing_evidence_count}")
    if bundle.stale_evidence_count > 0:
        errors.append(f"Stale evidence count: {bundle.stale_evidence_count}")
    return errors

def evidence_freeze_is_complete(bundle: NoOrderEvidenceFreezeBundle) -> bool:
    return len(validate_evidence_freeze_bundle_safety(bundle)) == 0

def evidence_freeze_requires_followup(bundle: NoOrderEvidenceFreezeBundle) -> bool:
    return not evidence_freeze_is_complete(bundle)

def evidence_freeze_blocks_next_stage(bundle: NoOrderEvidenceFreezeBundle) -> bool:
    return evidence_freeze_requires_followup(bundle)

def evidence_freeze_validator_summary(bundle: NoOrderEvidenceFreezeBundle) -> dict[str, Any]:
    return {"safe": evidence_freeze_is_complete(bundle), "errors": validate_evidence_freeze_bundle_safety(bundle)}

def evidence_freeze_validator_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
