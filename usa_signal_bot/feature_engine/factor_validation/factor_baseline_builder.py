import pandas as pd
from typing import Any
from datetime import datetime, timezone
import hashlib
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorDriftBaseline,
    create_factor_drift_baseline_id,
    validate_factor_drift_baseline
)

def compute_factor_baseline_stats(df: pd.DataFrame, factor_columns: list[str]) -> dict[str, dict[str, Any]]:
    stats = {}
    for c in factor_columns:
        if c not in df.columns:
            continue
        s = df[c]
        stats[c] = {
            "count": len(s),
            "finite_count": s.count(),
            "null_count": s.isna().sum(),
            "mean": s.mean() if not s.empty else None,
            "std": s.std() if not s.empty else None,
            "median": s.median() if not s.empty else None,
            "min": s.min() if not s.empty else None,
            "max": s.max() if not s.empty else None,
            "q05": s.quantile(0.05) if not s.empty else None,
            "q25": s.quantile(0.25) if not s.empty else None,
            "q75": s.quantile(0.75) if not s.empty else None,
            "q95": s.quantile(0.95) if not s.empty else None,
            "outlier_ratio": 0.0
        }
    return stats

def build_factor_drift_baseline(symbol: str, df: pd.DataFrame, factor_columns: list[str] | None = None) -> FactorDriftBaseline:
    if factor_columns is None:
        factor_columns = [c for c in df.columns if c not in ['symbol', 'timestamp', 'date', 'datetime']]

    stats = compute_factor_baseline_stats(df, factor_columns)
    hash_str = hashlib.sha256(pd.util.hash_pandas_object(df).values).hexdigest()

    baseline = FactorDriftBaseline(
        baseline_id=create_factor_drift_baseline_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        factor_columns=factor_columns,
        baseline_window_start=str(df['timestamp'].min()) if 'timestamp' in df.columns and not df.empty else None,
        baseline_window_end=str(df['timestamp'].max()) if 'timestamp' in df.columns and not df.empty else None,
        row_count=len(df),
        baseline_stats=stats,
        baseline_hash=hash_str,
        baseline_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_drift_baseline(baseline)
    return baseline

def build_factor_drift_baselines(tables: dict[str, pd.DataFrame]) -> list[FactorDriftBaseline]:
    return [build_factor_drift_baseline(sym, df) for sym, df in tables.items()]

def factor_baseline_builder_summary(baselines: list[FactorDriftBaseline]) -> dict[str, Any]:
    return {"baseline_count": len(baselines)}

def factor_baseline_builder_to_text(baselines: list[FactorDriftBaseline], limit: int = 100) -> str:
    return f"Built {len(baselines)} drift baselines."
