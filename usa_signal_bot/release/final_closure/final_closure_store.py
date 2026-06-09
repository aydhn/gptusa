from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from usa_signal_bot.release.final_closure.phase160_models import (
    FinalClosureContext,
    FinalClosureFullReview,
    FinalInputReference,
    FinalArtifactIndex,
    FinalPhaseLineage,
    FinalSystemAuditChecklist,
    FinalSystemAuditReport,
    FinalSafetyClosure,
    FinalLimitationRegister,
    FinalDocumentationIndex,
    FinalRunbookIndex,
    FinalTestEvidenceSummary,
    FinalQualityObservabilitySummary,
    FinalDeliveryCertificate,
    ProjectClosureReport,
    ProjectClosureManifest,
    FinalSafetyBoundaryResult,
    FinalClosureReadinessGate
)

def final_closure_store_dir(data_root: Path) -> Path:
    return data_root / "release" / "phase160"

def final_closure_contexts_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "contexts"

def final_closure_reviews_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "reviews"

def final_inputs_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "inputs"

def final_artifact_indexes_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_artifact_indexes"

def final_phase_lineage_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_phase_lineage"

def final_audit_checklists_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_audit_checklists"

def final_audit_reports_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_audit_reports"

def final_safety_closures_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_safety_closures"

def final_limitation_registers_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_limitation_registers"

def final_documentation_indexes_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_documentation_indexes"

def final_runbook_indexes_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_runbook_indexes"

def final_test_evidence_summaries_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_test_evidence_summaries"

def final_quality_observability_summaries_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_quality_observability_summaries"

def final_delivery_certificates_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_delivery_certificates"

def project_closure_reports_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "project_closure_reports"

def project_closure_manifests_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "project_closure_manifests"

def final_safety_boundaries_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_safety_boundaries"

def final_closure_readiness_gates_dir(data_root: Path) -> Path:
    return final_closure_store_dir(data_root) / "final_closure_readiness_gates"

def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def _write_json(path: Path, data: Dict[str, Any]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    return path

def write_final_closure_context_json(path: Path, item: FinalClosureContext) -> Path:
    return _write_json(path, item.to_dict())

def write_final_closure_full_review_json(path: Path, item: FinalClosureFullReview) -> Path:
    return _write_json(path, item.to_dict())

def write_final_input_refs_jsonl(path: Path, items: List[FinalInputReference]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item.to_dict()) + "\n")
    return path

def write_final_artifact_index_json(path: Path, item: FinalArtifactIndex) -> Path:
    return _write_json(path, item.to_dict())

def write_final_phase_lineage_json(path: Path, item: FinalPhaseLineage) -> Path:
    return _write_json(path, item.to_dict())

def write_final_system_audit_checklist_json(path: Path, item: FinalSystemAuditChecklist) -> Path:
    return _write_json(path, item.to_dict())

def write_final_system_audit_report_json(path: Path, item: FinalSystemAuditReport) -> Path:
    return _write_json(path, item.to_dict())

def write_final_safety_closure_json(path: Path, item: FinalSafetyClosure) -> Path:
    return _write_json(path, item.to_dict())

def write_final_limitation_register_json(path: Path, item: FinalLimitationRegister) -> Path:
    return _write_json(path, item.to_dict())

def write_final_documentation_index_json(path: Path, item: FinalDocumentationIndex) -> Path:
    return _write_json(path, item.to_dict())

def write_final_runbook_index_json(path: Path, item: FinalRunbookIndex) -> Path:
    return _write_json(path, item.to_dict())

def write_final_test_evidence_summary_json(path: Path, item: FinalTestEvidenceSummary) -> Path:
    return _write_json(path, item.to_dict())

def write_final_quality_observability_summary_json(path: Path, item: FinalQualityObservabilitySummary) -> Path:
    return _write_json(path, item.to_dict())

def write_final_delivery_certificate_json(path: Path, item: FinalDeliveryCertificate) -> Path:
    return _write_json(path, item.to_dict())

def write_project_closure_report_json(path: Path, item: ProjectClosureReport) -> Path:
    return _write_json(path, item.to_dict())

def write_project_closure_manifest_json(path: Path, item: ProjectClosureManifest) -> Path:
    return _write_json(path, item.to_dict())

def write_final_safety_boundary_json(path: Path, item: FinalSafetyBoundaryResult) -> Path:
    return _write_json(path, item.to_dict())

def write_final_closure_readiness_gate_json(path: Path, item: FinalClosureReadinessGate) -> Path:
    return _write_json(path, item.to_dict())

def read_final_closure_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_final_closure_reviews(data_root: Path) -> List[Path]:
    rev_dir = final_closure_reviews_dir(data_root)
    if not rev_dir.exists():
        return []
    return sorted(list(rev_dir.glob("*.json")))

def get_latest_final_closure_review(data_root: Path) -> Optional[Path]:
    revs = list_final_closure_reviews(data_root)
    return revs[-1] if revs else None

def final_closure_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_final_closure_reviews(data_root))
    }
