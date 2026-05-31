from typing import Any, Dict, List, Optional
from pathlib import Path
import json
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeFinalClosureContext,
    RegimeFinalClosureFullReview,
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    RegimeFinalSafetyAudit,
    MLInputContract,
    MLKickoffReadinessGate
)

def final_closure_store_dir(data_root: Path) -> Path:
    d = data_root / "regime_classification" / "final_closure"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_closure_contexts_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_closure_reviews_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def artifact_chain_validation_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "artifact_chain_validation"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_closure_results_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "final_closure_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def freeze_seals_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "freeze_seals"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_safety_audits_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "final_safety_audits"
    d.mkdir(parents=True, exist_ok=True)
    return d

def ml_input_contracts_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "ml_input_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def ml_kickoff_gates_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "ml_kickoff_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_regime_final_closure_context_json(path: Path, item: RegimeFinalClosureContext) -> Path:
    # mock logic for writing to json, real implementation would convert dataclass to dict
    with open(path, "w") as f:
        f.write("{}")
    return path

def write_regime_final_closure_full_review_json(path: Path, item: RegimeFinalClosureFullReview) -> Path:
    with open(path, "w") as f:
        f.write("{}")
    return path

def write_artifact_chain_validation_result_json(path: Path, item: RegimeArtifactChainValidationResult) -> Path:
    with open(path, "w") as f:
        f.write("{}")
    return path

def write_final_closure_result_json(path: Path, item: RegimeFinalClosureResult) -> Path:
    with open(path, "w") as f:
        f.write("{}")
    return path

def write_freeze_seal_json(path: Path, item: RegimeFreezeSeal) -> Path:
    with open(path, "w") as f:
        f.write("{}")
    return path

def write_final_safety_audit_json(path: Path, item: RegimeFinalSafetyAudit) -> Path:
    with open(path, "w") as f:
        f.write("{}")
    return path

def write_ml_input_contract_json(path: Path, item: MLInputContract) -> Path:
    with open(path, "w") as f:
        f.write("{}")
    return path

def write_ml_kickoff_readiness_gate_json(path: Path, item: MLKickoffReadinessGate) -> Path:
    with open(path, "w") as f:
        f.write("{}")
    return path

def read_regime_final_closure_full_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def list_regime_final_closure_reviews(data_root: Path) -> List[Path]:
    d = final_closure_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_regime_final_closure_review(data_root: Path) -> Optional[Path]:
    files = list_regime_final_closure_reviews(data_root)
    if not files:
        return None
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[0]

def final_closure_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews_count": len(list_regime_final_closure_reviews(data_root))}
