import pandas as pd
from typing import Any
from datetime import datetime, timezone
import hashlib
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorSchemaSignature,
    create_factor_schema_signature_id,
    validate_factor_schema_signature
)
from usa_signal_bot.feature_engine.factor_validation.factor_persistence_safety_validator import factor_persistence_columns_safety

def stable_schema_hash(columns: list[str], factor_columns: list[str]) -> str:
    s = "".join(sorted(columns)) + "".join(sorted(factor_columns))
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def build_factor_schema_signature(symbol: str | None, df: pd.DataFrame, schema_version: str = "phase122.v1") -> FactorSchemaSignature:
    cols = list(df.columns)
    factor_cols = [c for c in cols if c not in ['symbol', 'timestamp', 'date', 'datetime']]

    forbidden = factor_persistence_columns_safety(cols)

    sig = FactorSchemaSignature(
        signature_id=create_factor_schema_signature_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        required_columns=[c for c in cols if c in ['symbol', 'timestamp']],
        factor_columns=factor_cols,
        raw_factor_columns=[],
        normalized_factor_columns=[],
        percentile_factor_columns=[],
        rank_factor_columns=[],
        diagnostics_columns=[],
        schema_hash=stable_schema_hash(cols, factor_cols),
        schema_version=schema_version,
        schema_valid=len(forbidden) == 0,
        forbidden_columns_present=forbidden,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_schema_signature(sig)
    return sig

def compare_factor_schema_signatures(old: FactorSchemaSignature, new: FactorSchemaSignature) -> dict[str, Any]:
    return {"match": old.schema_hash == new.schema_hash}

def factor_schema_signature_summary(signatures: list[FactorSchemaSignature]) -> dict[str, Any]:
    return {"signature_count": len(signatures)}

def factor_schema_signature_to_text(signature: FactorSchemaSignature) -> str:
    return f"Schema {signature.signature_id}: valid={signature.schema_valid}"
