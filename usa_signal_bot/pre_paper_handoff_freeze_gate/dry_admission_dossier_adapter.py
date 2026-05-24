from typing import Any, Tuple, List
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import PrePaperHandoffFreezeFullReview

def handoff_freeze_evidence_from_dry_admission_dossier(payload: dict[str, Any]) -> List[str]:
    return []

def dry_admission_dossier_supports_handoff_freeze(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    return len(warnings) == 0, warnings

def attach_handoff_freeze_hint_to_dry_admission_dossier_payload(payload: dict[str, Any], review: PrePaperHandoffFreezeFullReview) -> dict[str, Any]:
    res = dict(payload)
    res["pre_paper_handoff_freeze_hint"] = {
        "review_id": review.review_id,
        "frozen": True
    }
    return res

def dry_admission_dossier_handoff_freeze_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("pre_paper_handoff_freeze_hint", {})

def dry_admission_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Dry Admission Dossier Adapter: {dry_admission_dossier_handoff_freeze_summary(payload)}"
