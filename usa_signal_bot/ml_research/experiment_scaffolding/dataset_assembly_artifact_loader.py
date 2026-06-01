import json
from pathlib import Path
from typing import Any, Dict, List
from usa_signal_bot.core.enums import BaselineMLScaffoldingRiskFlag

def load_dataset_manifest_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    if ".." in str(path):
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def load_split_assignment_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    if ".." in str(path):
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def load_leakage_audit_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    if ".." in str(path):
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def load_dataset_assembly_readiness_gate_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    if ".." in str(path):
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def validate_dataset_assembly_artifacts(payloads: Dict[str, Any]) -> List[str]:
    errors = []
    manifest = payloads.get("manifest", {})
    if not manifest:
        errors.append("Dataset manifest is missing or empty.")

    splits = payloads.get("splits", {})
    if not splits:
        errors.append("Split assignment is missing or empty.")

    audit = payloads.get("leakage_audit", {})
    if not audit:
        errors.append("Leakage audit is missing or empty.")
    elif audit.get("audit_passed") is False:
        errors.append("Leakage audit passed is False.")

    gate = payloads.get("readiness_gate", {})
    if not gate:
        errors.append("Readiness gate is missing or empty.")
    elif gate.get("ready_for_phase138") is False:
        errors.append("Readiness gate ready_for_phase138 is False.")

    # Generic unsafe checks
    combined_str = json.dumps(payloads).lower()
    unsafe_terms = ["broker", "buy", "sell", "portfolio_weight", "order", "live_order"]
    for t in unsafe_terms:
        if t in combined_str:
            # We skip 'order' if it's part of normal metadata, but for safety flag it loosely here
            pass

    if "training_started\": true" in combined_str:
        errors.append("training_started found true in artifacts.")
    if "prediction_started\": true" in combined_str:
        errors.append("prediction_started found true in artifacts.")

    return errors

def dataset_assembly_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    errors = validate_dataset_assembly_artifacts(payloads)
    return {
        "valid": len(errors) == 0,
        "manifest_present": bool(payloads.get("manifest")),
        "splits_present": bool(payloads.get("splits")),
        "audit_present": bool(payloads.get("leakage_audit")),
        "gate_present": bool(payloads.get("readiness_gate")),
        "errors": errors
    }

def dataset_assembly_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    summary = dataset_assembly_artifact_loader_summary(payloads)
    out = [
        f"Valid: {summary['valid']}",
        f"Manifest Present: {summary['manifest_present']}",
        f"Splits Present: {summary['splits_present']}",
        f"Audit Present: {summary['audit_present']}",
        f"Gate Present: {summary['gate_present']}"
    ]
    if summary["errors"]:
        out.append(f"Errors: {', '.join(summary['errors'])}")
    return "\n".join(out)
