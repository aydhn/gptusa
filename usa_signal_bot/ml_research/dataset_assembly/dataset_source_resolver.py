import hashlib
from typing import Any, Dict, List, Optional
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetSourceReference,
    MLDatasetSourceResolutionStatus,
    MLDatasetAssemblyRiskFlag,
    create_ml_dataset_source_reference_id,
    ml_dataset_source_reference_to_dict
)
import json

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def compute_source_file_hash(path: Path) -> Optional[str]:
    if not path.exists() or not path.is_file():
        return None
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def inspect_local_csv_source(path: Path, required_columns: Optional[List[str]] = None) -> Dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {"status": "MISSING", "error": "File not found"}
    try:
        df = pd.read_csv(path, nrows=5)
        columns = list(df.columns)
        missing = []
        if required_columns:
            missing = [c for c in required_columns if c not in columns]

        forbidden = ["buy", "sell", "order", "portfolio_weight", "target_weight", "allocation", "paper", "live_order"]
        has_forbidden = any(any(f in c.lower() for f in forbidden) for c in columns)

        with open(path, "rb") as f:
            row_count = sum(chunk.count(b"\n") for chunk in iter(lambda: f.read(1024 * 1024), b"")) - 1 # rough estimate

        return {
            "status": "RESOLVED" if not missing else "PARTIALLY_RESOLVED",
            "columns": columns,
            "missing_columns": missing,
            "row_count": row_count,
            "column_count": len(columns),
            "contains_forbidden_outputs": has_forbidden
        }
    except Exception as e:
        return {"status": "INVALID", "error": str(e)}

def resolve_source_reference(source_payload: Dict[str, Any], base_dir: Optional[Path] = None) -> MLDatasetSourceReference:
    source_name = source_payload.get("source_name", "unknown")
    source_path_str = source_payload.get("source_path")
    required_columns = source_payload.get("required_columns", [])

    ref = MLDatasetSourceReference(
        source_ref_id=create_ml_dataset_source_reference_id(),
        created_at_utc=_now(),
        source_name=source_name,
        source_kind=source_payload.get("source_kind", "CSV"),
        source_path=source_path_str,
        source_resolution_status=MLDatasetSourceResolutionStatus.UNKNOWN,
        source_artifact_kind=None,
        row_count=None,
        column_count=None,
        source_hash=None, required_columns=required_columns
    )

    if not source_path_str:
        ref.source_resolution_status = MLDatasetSourceResolutionStatus.MISSING
        ref.errors.append("source_path is empty")
        return ref

    p = Path(source_path_str)
    if base_dir and not p.is_absolute():
        p = base_dir / p

    if ".." in str(p):
        ref.source_resolution_status = MLDatasetSourceResolutionStatus.BLOCKED
        ref.errors.append("Path traversal detected")
        return ref

    ref.source_hash = compute_source_file_hash(p)
    inspection = inspect_local_csv_source(p, required_columns)

    if inspection.get("status") == "MISSING":
        ref.source_resolution_status = MLDatasetSourceResolutionStatus.MISSING
        ref.errors.append(inspection.get("error", "File not found"))
    elif inspection.get("status") == "INVALID":
        ref.source_resolution_status = MLDatasetSourceResolutionStatus.INVALID
        ref.errors.append(inspection.get("error", "Invalid file format"))
    else:
        ref.source_resolution_status = MLDatasetSourceResolutionStatus(inspection.get("status", "UNKNOWN"))
        ref.available_columns = inspection.get("columns", [])
        ref.missing_columns = inspection.get("missing_columns", [])
        ref.row_count = inspection.get("row_count")
        ref.column_count = inspection.get("column_count")
        ref.contains_forbidden_outputs = inspection.get("contains_forbidden_outputs", False)

        if ref.contains_forbidden_outputs:
            ref.risk_flags.append(MLDatasetAssemblyRiskFlag.FORBIDDEN_DATASET_ASSEMBLY_COLUMN)

    return ref

def resolve_dataset_sources(source_registry_payload: Dict[str, Any], base_dir: Optional[Path] = None) -> List[MLDatasetSourceReference]:
    sources = source_registry_payload.get("sources", [])
    return [resolve_source_reference(s, base_dir) for s in sources]

def validate_dataset_source_references(refs: List[MLDatasetSourceReference]) -> List[str]:
    errors = []
    for ref in refs:
        if ref.source_resolution_status != MLDatasetSourceResolutionStatus.RESOLVED:
            errors.append(f"Source {ref.source_name} is not resolved: {ref.source_resolution_status.value}")
        if ref.contains_forbidden_outputs:
            errors.append(f"Source {ref.source_name} contains forbidden outputs")
    return errors

def dataset_source_resolution_summary(refs: List[MLDatasetSourceReference]) -> Dict[str, Any]:
    return {
        "total_sources": len(refs),
        "resolved_sources": sum(1 for r in refs if r.source_resolution_status == MLDatasetSourceResolutionStatus.RESOLVED),
        "missing_sources": sum(1 for r in refs if r.source_resolution_status == MLDatasetSourceResolutionStatus.MISSING),
        "invalid_sources": sum(1 for r in refs if r.source_resolution_status == MLDatasetSourceResolutionStatus.INVALID)
    }

def dataset_source_resolution_to_text(refs: List[MLDatasetSourceReference], limit: int = 300) -> str:
    s = json.dumps(dataset_source_resolution_summary(refs), indent=2)
    if len(s) > limit:
        return s[:limit] + "..."
    return s
