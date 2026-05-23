import json
from pathlib import Path
from typing import Any, Optional
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    NoWriteTransitionDossier,
    TransitionDossierEvidenceItem,
    AdmissionEvidenceSealValidation,
    AdmissionEvidenceSealRefresh,
    PaperSandboxBridgeRoute,
    PaperSandboxBridgeEnvelope,
    NoWriteTransitionAuditEntry,
    NoWriteTransitionFullReview,
    no_write_transition_dossier_to_dict,
    transition_dossier_evidence_item_to_dict,
    admission_evidence_seal_validation_to_dict,
    admission_evidence_seal_refresh_to_dict,
    paper_sandbox_bridge_route_to_dict,
    paper_sandbox_bridge_envelope_to_dict,
    no_write_transition_audit_entry_to_dict,
    no_write_transition_full_review_to_dict
)
def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path, data):
    import json
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def read_json(path):
    import json
    with open(path, "r") as f:
        return json.load(f)


class JSONLStore:
    def __init__(self, directory):
        self.directory = directory
    def append_batch(self, filename, items):
        import json
        with open(self.directory / filename, "a") as f:
            for item in items:
                f.write(json.dumps(item) + "\n")


def no_write_transition_store_dir(data_root: Path) -> Path:
    return ensure_dir(data_root / "paper_no_write_transition")

def transition_dossiers_dir(data_root: Path) -> Path:
    return ensure_dir(no_write_transition_store_dir(data_root) / "dossiers")

def transition_evidence_dir(data_root: Path) -> Path:
    return ensure_dir(no_write_transition_store_dir(data_root) / "evidence")

def evidence_seal_validations_dir(data_root: Path) -> Path:
    return ensure_dir(no_write_transition_store_dir(data_root) / "seal_validations")

def evidence_seal_refreshes_dir(data_root: Path) -> Path:
    return ensure_dir(no_write_transition_store_dir(data_root) / "seal_refreshes")

def sandbox_bridge_envelopes_dir(data_root: Path) -> Path:
    return ensure_dir(no_write_transition_store_dir(data_root) / "sandbox_bridge_envelopes")

def sandbox_bridge_routes_dir(data_root: Path) -> Path:
    return ensure_dir(no_write_transition_store_dir(data_root) / "sandbox_bridge_routes")

def transition_audit_dir(data_root: Path) -> Path:
    return ensure_dir(no_write_transition_store_dir(data_root) / "audit")

def transition_full_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(no_write_transition_store_dir(data_root) / "full_reviews")


def write_transition_dossier_json(path: Path, item: NoWriteTransitionDossier) -> Path:
    write_json(path, no_write_transition_dossier_to_dict(item))
    return path

def write_transition_evidence_jsonl(path: Path, items: list[TransitionDossierEvidenceItem]) -> Path:
    store = JSONLStore(path.parent)
    dicts = [transition_dossier_evidence_item_to_dict(i) for i in items]
    store.append_batch(path.name, dicts)
    return path

def write_evidence_seal_validation_json(path: Path, item: AdmissionEvidenceSealValidation) -> Path:
    write_json(path, admission_evidence_seal_validation_to_dict(item))
    return path

def write_evidence_seal_refresh_json(path: Path, item: AdmissionEvidenceSealRefresh) -> Path:
    write_json(path, admission_evidence_seal_refresh_to_dict(item))
    return path

def write_sandbox_bridge_envelope_json(path: Path, item: PaperSandboxBridgeEnvelope) -> Path:
    write_json(path, paper_sandbox_bridge_envelope_to_dict(item))
    return path

def write_sandbox_bridge_routes_jsonl(path: Path, items: list[PaperSandboxBridgeRoute]) -> Path:
    store = JSONLStore(path.parent)
    dicts = [paper_sandbox_bridge_route_to_dict(i) for i in items]
    store.append_batch(path.name, dicts)
    return path

def write_transition_audit_jsonl(path: Path, items: list[NoWriteTransitionAuditEntry]) -> Path:
    store = JSONLStore(path.parent)
    dicts = [no_write_transition_audit_entry_to_dict(i) for i in items]
    store.append_batch(path.name, dicts)
    return path

def write_no_write_transition_full_review_json(path: Path, item: NoWriteTransitionFullReview) -> Path:
    write_json(path, no_write_transition_full_review_to_dict(item))
    return path

def read_no_write_transition_full_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

def list_no_write_transition_full_reviews(data_root: Path) -> list[Path]:
    d = transition_full_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_no_write_transition_full_review(data_root: Path) -> Optional[Path]:
    files = list_no_write_transition_full_reviews(data_root)
    return files[-1] if files else None

def no_write_transition_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "full_reviews": len(list_no_write_transition_full_reviews(data_root))
    }
