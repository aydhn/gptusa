import os

path1 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_gate_adapter.py"
content1 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionGateDossier, DryAdmissionAcceptanceSeal, PaperModeRehearsalBlockerEvent, DryAdmissionDossierFullReview
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier import build_dry_admission_gate_dossier
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_report import build_dry_admission_dossier_full_review

def dry_admission_dossier_from_gate(payload: dict[str, Any]) -> DryAdmissionGateDossier:
    return build_dry_admission_gate_dossier(payload)

def dry_admission_acceptance_seal_from_gate(payload: dict[str, Any]) -> DryAdmissionAcceptanceSeal:
    return build_dry_admission_gate_dossier(payload).acceptance_seal

def rehearsal_blocker_events_from_gate(payload: dict[str, Any]) -> list[PaperModeRehearsalBlockerEvent]:
    return build_dry_admission_gate_dossier(payload).rehearsal_blocker_events

def dry_admission_dossier_full_review_from_gate(payload: dict[str, Any]) -> DryAdmissionDossierFullReview:
    return build_dry_admission_dossier_full_review(payload)

def attach_dry_admission_dossier_metadata_to_gate_payload(payload: dict[str, Any], review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    payload["dry_admission_dossier_review_id"] = review.review_id
    payload["dry_admission_dossier_metadata"] = {
        "status": review.dossiers[0].status.value if review.dossiers else "UNKNOWN",
        "seal_sealed": review.acceptance_seals[0].sealed if review.acceptance_seals else False
    }
    return payload

def dry_admission_gate_dossier_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("dry_admission_dossier_metadata", {})

def dry_admission_gate_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = dry_admission_gate_dossier_summary(payload)
    return f"Gate Adapter: {summary}"
"""

path2 = "usa_signal_bot/paper_mode_dry_admission_dossier/board_dossier_adapter.py"
content2 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionDossierFullReview

def dry_admission_dossier_evidence_from_board_dossier(payload: dict[str, Any]) -> list[str]:
    return [payload.get("board_dossier_id")] if payload.get("board_dossier_id") else []

def board_dossier_supports_dry_admission_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if not payload.get("board_dossier_id"):
        reasons.append("No board dossier id")
    return len(reasons) == 0, reasons

def attach_dry_admission_dossier_hint_to_board_dossier_payload(payload: dict[str, Any], review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    payload["dry_admission_dossier_hint"] = review.review_id
    return payload

def board_dossier_dry_admission_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"hint": payload.get("dry_admission_dossier_hint")}

def board_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = board_dossier_dry_admission_summary(payload)
    return f"Board Dossier Adapter: {summary}"
"""

path3 = "usa_signal_bot/paper_mode_dry_admission_dossier/non_execution_board_adapter.py"
content3 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionDossierFullReview

def dry_admission_dossier_evidence_from_non_execution_board(payload: dict[str, Any]) -> list[str]:
    return [payload.get("non_execution_board_id")] if payload.get("non_execution_board_id") else []

def non_execution_board_supports_dry_admission_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if not payload.get("non_execution_board_id"):
        reasons.append("No non-execution board id")
    return len(reasons) == 0, reasons

def attach_dry_admission_dossier_hint_to_non_execution_board_payload(payload: dict[str, Any], review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    payload["dry_admission_dossier_hint"] = review.review_id
    return payload

def non_execution_board_dry_admission_dossier_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"hint": payload.get("dry_admission_dossier_hint")}

def non_execution_board_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = non_execution_board_dry_admission_dossier_summary(payload)
    return f"Non-Execution Board Adapter: {summary}"
"""

path4 = "usa_signal_bot/paper_mode_dry_admission_dossier/paper_runtime_adapter.py"
content4 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import DryAdmissionDossierFullReview

def build_read_only_paper_snapshot_for_dry_admission_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = paper_payload or {}
    return {
        "paper_state_committed": False,
        "paper_order_executed": False,
        "portfolio_state_mutated": False,
        "is_read_only_snapshot": True,
        "original_payload_keys": list(payload.keys())
    }

def build_rehearsal_blocker_snapshot_for_dry_admission_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_read_only_paper_snapshot_for_dry_admission_dossier(paper_payload)

def compare_dry_admission_dossier_to_paper_snapshot(review: DryAdmissionDossierFullReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "snapshot_read_only": paper_snapshot.get("is_read_only_snapshot", False),
        "mutation_risk": not paper_snapshot.get("is_read_only_snapshot", False)
    }

def validate_paper_runtime_not_mutated_by_dry_admission_dossier(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    errors = []
    if before.get("paper_state_committed") != after.get("paper_state_committed"):
        errors.append("Paper state committed changed")
    if before.get("paper_order_executed") != after.get("paper_order_executed"):
        errors.append("Paper order executed changed")
    if before.get("portfolio_state_mutated") != after.get("portfolio_state_mutated"):
        errors.append("Portfolio state mutated changed")
    return errors

def attach_dry_admission_dossier_metadata_to_paper_analytics(payload: dict[str, Any], review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    payload["dry_admission_dossier_review_id"] = review.review_id
    return payload

def paper_runtime_dry_admission_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    return f"Paper Runtime Adapter: {payload.get('dry_admission_dossier_review_id')}"
"""

with open(path1, "w") as f:
    f.write(content1)
with open(path2, "w") as f:
    f.write(content2)
with open(path3, "w") as f:
    f.write(content3)
with open(path4, "w") as f:
    f.write(content4)

print("Adapters created")
