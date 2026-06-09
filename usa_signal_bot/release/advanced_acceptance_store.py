from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import dataclasses

from usa_signal_bot.release.phase159_models import (
    AdvancedAcceptanceContext,
    AdvancedAcceptanceFullReview,
    AdvancedAcceptanceInputReference,
    AcceptanceScenarioMatrix,
    AdvancedDryRunStep,
    AcceptanceEvidenceBundle,
    AcceptanceAreaReport,
    ReleaseCandidateRiskRegister,
    ReleaseCandidateAudit,
    FinalFreezeChecklist,
    FinalFreezeBoundaryResult,
    FinalFreezeCertificate,
    Phase160HandoffContract,
    Phase160HandoffPackage,
    Phase160ReadinessGate
)

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if hasattr(o, "value"):
            return o.value
        return super().default(o)

def _write_json(path: Path, item: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(item, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def _write_jsonl(path: Path, items: List[Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\n")
    return path

def advanced_acceptance_store_dir(data_root: Path) -> Path:
    return data_root / "release" / "phase159"

def advanced_acceptance_contexts_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "contexts"

def advanced_acceptance_reviews_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "reviews"

def acceptance_inputs_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "inputs"

def scenario_matrices_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "scenario_matrices"

def dry_run_transcripts_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "dry_run_transcripts"

def evidence_bundles_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "evidence_bundles"

def area_reports_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "area_reports"

def risk_registers_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "risk_registers"

def release_candidate_audits_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "release_candidate_audits"

def final_freeze_checklists_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "final_freeze_checklists"

def final_freeze_boundaries_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "final_freeze_boundaries"

def final_freeze_certificates_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "final_freeze_certificates"

def phase160_handoff_contracts_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "phase160_handoff_contracts"

def phase160_handoff_packages_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "phase160_handoff_packages"

def phase160_gates_dir(data_root: Path) -> Path:
    return advanced_acceptance_store_dir(data_root) / "phase160_gates"

def write_advanced_acceptance_context_json(path: Path, item: AdvancedAcceptanceContext) -> Path:
    return _write_json(path, item)

def write_advanced_acceptance_full_review_json(path: Path, item: AdvancedAcceptanceFullReview) -> Path:
    return _write_json(path, item)

def write_advanced_acceptance_input_refs_jsonl(path: Path, items: List[AdvancedAcceptanceInputReference]) -> Path:
    return _write_jsonl(path, items)

def write_acceptance_scenario_matrix_json(path: Path, item: AcceptanceScenarioMatrix) -> Path:
    return _write_json(path, item)

def write_advanced_dry_run_steps_jsonl(path: Path, items: List[AdvancedDryRunStep]) -> Path:
    return _write_jsonl(path, items)

def write_acceptance_evidence_bundle_json(path: Path, item: AcceptanceEvidenceBundle) -> Path:
    return _write_json(path, item)

def write_acceptance_area_reports_jsonl(path: Path, items: List[AcceptanceAreaReport]) -> Path:
    return _write_jsonl(path, items)

def write_release_candidate_risk_register_json(path: Path, item: ReleaseCandidateRiskRegister) -> Path:
    return _write_json(path, item)

def write_release_candidate_audit_json(path: Path, item: ReleaseCandidateAudit) -> Path:
    return _write_json(path, item)

def write_final_freeze_checklist_json(path: Path, item: FinalFreezeChecklist) -> Path:
    return _write_json(path, item)

def write_final_freeze_boundary_json(path: Path, item: FinalFreezeBoundaryResult) -> Path:
    return _write_json(path, item)

def write_final_freeze_certificate_json(path: Path, item: FinalFreezeCertificate) -> Path:
    return _write_json(path, item)

def write_phase160_handoff_contract_json(path: Path, item: Phase160HandoffContract) -> Path:
    return _write_json(path, item)

def write_phase160_handoff_package_json(path: Path, item: Phase160HandoffPackage) -> Path:
    return _write_json(path, item)

def write_phase160_readiness_gate_json(path: Path, item: Phase160ReadinessGate) -> Path:
    return _write_json(path, item)

def read_advanced_acceptance_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_advanced_acceptance_reviews(data_root: Path) -> List[Path]:
    d = advanced_acceptance_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted(d.glob("*.json"))

def get_latest_advanced_acceptance_review(data_root: Path) -> Optional[Path]:
    files = list_advanced_acceptance_reviews(data_root)
    return files[-1] if files else None

def advanced_acceptance_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_advanced_acceptance_reviews(data_root))
    }
