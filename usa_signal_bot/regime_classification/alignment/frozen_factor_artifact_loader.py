from typing import Any
import json
import pandas as pd
from pathlib import Path
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    FrozenFactorAlignmentReference, create_frozen_factor_alignment_reference_id, _now
)
from usa_signal_bot.core.enums import RegimeAlignmentRiskFlag

def load_final_closure_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def load_frozen_factor_table_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    if ".." in str(path):
        raise ValueError("Path traversal detected")
    return pd.read_csv(path)

def load_frozen_factor_tables(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    res = {}
    for sym, p in paths.items():
        res[sym] = load_frozen_factor_table_csv(p)
    return res

def build_frozen_factor_alignment_references(manifest_payload: dict[str, Any] | None, tables: dict[str, pd.DataFrame] | None = None) -> list[FrozenFactorAlignmentReference]:
    refs = []
    if manifest_payload:
        for ref_data in manifest_payload.get("artifact_references", []):
            refs.append(FrozenFactorAlignmentReference(
                reference_id=create_frozen_factor_alignment_reference_id(),
                created_at_utc=_now(),
                symbol=ref_data.get("symbol"),
                artifact_name=ref_data.get("artifact_name", "unknown"),
                artifact_path=ref_data.get("artifact_path"),
                artifact_hash=ref_data.get("artifact_hash"),
                factor_columns=[], feature_columns=[],
                available=True
            ))

    if tables:
        for sym, df in tables.items():
            refs.append(FrozenFactorAlignmentReference(
                reference_id=create_frozen_factor_alignment_reference_id(),
                created_at_utc=_now(),
                symbol=sym,
                artifact_name=f"table_{sym}",
                artifact_path=None,
                artifact_hash=None,
                factor_columns=infer_factor_columns(df),
                feature_columns=infer_feature_columns(df),
                available=True
            ))

    if not refs:
         refs.append(FrozenFactorAlignmentReference(
                reference_id=create_frozen_factor_alignment_reference_id(),
                created_at_utc=_now(),
                symbol=None,
                artifact_name="missing",
                artifact_path=None,
                artifact_hash=None,
                available=False,
                risk_flags=[RegimeAlignmentRiskFlag.FROZEN_FACTOR_ARTIFACT_MISSING]
            ))
    return refs

def infer_factor_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if "factor" in c.lower()]

def infer_feature_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if "feature" in c.lower() or "indicator" in c.lower()]

def validate_frozen_factor_alignment_references(refs: list[FrozenFactorAlignmentReference]) -> list[str]:
    errors = []
    for r in refs:
        if not r.available:
            errors.append(f"Ref {r.reference_id} missing")
        for col in r.factor_columns + r.feature_columns:
            cl = col.lower()
            if any(x in cl for x in ["buy", "sell", "order", "broker", "portfolio", "weight", "allocation"]):
                if cl != "macd_signal_9":
                    errors.append(f"Forbidden column {col} in {r.reference_id}")
    return errors

def frozen_factor_artifact_loader_summary(refs: list[FrozenFactorAlignmentReference]) -> dict[str, Any]:
    return {"count": len(refs), "available": sum(1 for r in refs if r.available)}

def frozen_factor_artifact_loader_to_text(refs: list[FrozenFactorAlignmentReference], limit: int = 200) -> str:
    return f"Loaded {len(refs)} frozen factor refs."
