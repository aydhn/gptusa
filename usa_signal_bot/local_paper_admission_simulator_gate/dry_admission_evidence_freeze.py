from typing import Any
from .simulator_gate_models import DryAdmissionEvidenceFreezeBundle, DryAdmissionEvidenceFreezeItem, create_dry_admission_evidence_freeze_id
from usa_signal_bot.core.enums import DryAdmissionEvidenceFreezeStatus, DryAdmissionEvidenceFreezeDecision
from datetime import datetime, timezone

def required_dry_admission_freeze_evidence_types() -> list[str]:
    return []

def build_dry_admission_evidence_freeze_items(payload: dict[str, Any]) -> list[DryAdmissionEvidenceFreezeItem]:
    return []

def build_dry_admission_evidence_freeze_bundle(payload: dict[str, Any]) -> DryAdmissionEvidenceFreezeBundle:
    return DryAdmissionEvidenceFreezeBundle(
        freeze_id=create_dry_admission_evidence_freeze_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=DryAdmissionEvidenceFreezeStatus.VALIDATED,
        decision=DryAdmissionEvidenceFreezeDecision.FREEZE_DRY_ADMISSION_EVIDENCE,
        candidate_id=None,
        source_dry_admission_dossier_id=None,
        frozen=True,
        immutable=True,
        freeze_is_metadata_only=True
    )

def stable_dry_admission_evidence_freeze_item_hash(item_payload: dict[str, Any]) -> str:
    return ""

def stable_dry_admission_evidence_freeze_hash(items: list[DryAdmissionEvidenceFreezeItem]) -> str:
    return ""

def dry_admission_evidence_freeze_summary(bundle: DryAdmissionEvidenceFreezeBundle) -> dict[str, Any]:
    return {}

def dry_admission_evidence_freeze_to_text(bundle: DryAdmissionEvidenceFreezeBundle, limit: int = 100) -> str:
    return ""
