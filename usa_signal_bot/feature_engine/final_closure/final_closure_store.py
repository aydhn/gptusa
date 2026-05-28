import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FinalClosureContext, FinalClosureFullReview, FinalClosureManifest,
    FreezeSealMetadata, EngineReadinessCertificate, Phase126KickoffGate,
    FinalClosureAudit, final_closure_context_to_dict, final_closure_full_review_to_dict,
    final_closure_manifest_to_dict, freeze_seal_metadata_to_dict,
    engine_readiness_certificate_to_dict, phase126_kickoff_gate_to_dict,
    final_closure_audit_to_dict
)

def final_closure_store_dir(data_root: Path) -> Path:
    d = data_root / "feature_engine" / "final_closure"
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

def final_closure_manifests_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "manifests"
    d.mkdir(parents=True, exist_ok=True)
    return d

def freeze_seals_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "freeze_seals"
    d.mkdir(parents=True, exist_ok=True)
    return d

def engine_certificates_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "certificates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def phase126_kickoff_gates_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "phase126_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_closure_audits_dir(data_root: Path) -> Path:
    d = final_closure_store_dir(data_root) / "audits"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_final_closure_context_json(path: Path, item: FinalClosureContext) -> Path:
    with open(path, "w") as f:
        json.dump(final_closure_context_to_dict(item), f, indent=2)
    return path

def write_final_closure_full_review_json(path: Path, item: FinalClosureFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(final_closure_full_review_to_dict(item), f, indent=2)
    return path

def write_final_closure_manifest_json(path: Path, item: FinalClosureManifest) -> Path:
    with open(path, "w") as f:
        json.dump(final_closure_manifest_to_dict(item), f, indent=2)
    return path

def write_freeze_seal_metadata_json(path: Path, item: FreezeSealMetadata) -> Path:
    with open(path, "w") as f:
        json.dump(freeze_seal_metadata_to_dict(item), f, indent=2)
    return path

def write_engine_readiness_certificate_json(path: Path, item: EngineReadinessCertificate) -> Path:
    with open(path, "w") as f:
        json.dump(engine_readiness_certificate_to_dict(item), f, indent=2)
    return path

def write_phase126_kickoff_gate_json(path: Path, item: Phase126KickoffGate) -> Path:
    with open(path, "w") as f:
        json.dump(phase126_kickoff_gate_to_dict(item), f, indent=2)
    return path

def write_final_closure_audit_json(path: Path, item: FinalClosureAudit) -> Path:
    with open(path, "w") as f:
        json.dump(final_closure_audit_to_dict(item), f, indent=2)
    return path

def read_final_closure_full_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def list_final_closure_reviews(data_root: Path) -> List[Path]:
    d = final_closure_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_final_closure_review(data_root: Path) -> Optional[Path]:
    reviews = list_final_closure_reviews(data_root)
    if reviews:
        return reviews[-1]
    return None

def final_closure_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_final_closure_reviews(data_root))
    }
