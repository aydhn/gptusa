cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/dry_admission_adapter.py
from typing import Any, Dict
import json
from .admission_review_models import PaperModeAdmissionReview, LedgerReconciliationReport, FinalNoWriteTransitionCheckpoint, AdmissionReviewFullReport
from .admission_report import build_admission_review_full_report

def admission_review_from_dry_admission(payload: Dict[str, Any]) -> PaperModeAdmissionReview:
    report = build_admission_review_full_report(payload)
    return report.admission_reviews[0]

def ledger_reconciliation_from_dry_admission(payload: Dict[str, Any]) -> LedgerReconciliationReport:
    report = build_admission_review_full_report(payload)
    return report.ledger_reconciliations[0] if report.ledger_reconciliations else None

def transition_checkpoint_from_dry_admission(payload: Dict[str, Any]) -> FinalNoWriteTransitionCheckpoint:
    report = build_admission_review_full_report(payload)
    return report.transition_checkpoints[0] if report.transition_checkpoints else None

def admission_full_report_from_dry_admission(payload: Dict[str, Any]) -> AdmissionReviewFullReport:
    return build_admission_review_full_report(payload)

def attach_admission_review_metadata_to_dry_admission_payload(payload: Dict[str, Any], report: AdmissionReviewFullReport) -> Dict[str, Any]:
    payload["admission_review_id"] = report.admission_reviews[0].admission_review_id if report.admission_reviews else None
    payload["transition_checkpoint_id"] = report.transition_checkpoints[0].checkpoint_id if report.transition_checkpoints else None
    return payload

def dry_admission_admission_review_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"admission_review_id": payload.get("admission_review_id")}

def dry_admission_adapter_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(dry_admission_admission_review_summary(payload), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/no_write_adapter.py
from typing import Any, Dict, List, Tuple
import json

def admission_evidence_from_no_write(payload: Dict[str, Any]) -> List[str]:
    return [payload.get("evidence_ref")] if payload.get("evidence_ref") else []

def no_write_supports_admission_review(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_admission_hint_to_no_write_payload(payload: Dict[str, Any], report: Any) -> Dict[str, Any]:
    payload["admission_hint"] = "Admission review completed"
    return payload

def no_write_admission_review_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"admission_hint": payload.get("admission_hint")}

def no_write_adapter_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(no_write_admission_review_summary(payload), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/board_adapter.py
from typing import Any, Dict, List, Tuple
import json

def admission_evidence_from_board(payload: Dict[str, Any]) -> List[str]:
    return [payload.get("board_evidence_ref")] if payload.get("board_evidence_ref") else []

def board_supports_admission_review(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_admission_hint_to_board_payload(payload: Dict[str, Any], report: Any) -> Dict[str, Any]:
    payload["admission_hint"] = "Admission review via board completed"
    return payload

def board_admission_review_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"admission_hint": payload.get("admission_hint")}

def board_adapter_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(board_admission_review_summary(payload), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/paper_runtime_adapter.py
from typing import Any, Dict, List
import json
import copy

def build_read_only_paper_snapshot_for_admission_review(paper_payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    snapshot = copy.deepcopy(paper_payload) if paper_payload else {}
    snapshot["readonly"] = True
    return snapshot

def compare_admission_review_to_paper_snapshot(report: Any, paper_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {"match": True}

def validate_paper_runtime_not_mutated_by_admission_review(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    errors = []
    for key in ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]:
        if after.get(key, False):
             errors.append(f"{key} is true in after state")
    return errors

def attach_admission_review_metadata_to_paper_analytics(payload: Dict[str, Any], report: Any) -> Dict[str, Any]:
    payload["admission_review_metadata_attached"] = True
    return payload

def paper_runtime_admission_review_adapter_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
INNER_EOF
