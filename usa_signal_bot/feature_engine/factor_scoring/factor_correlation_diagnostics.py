from typing import Any
import pandas as pd
import numpy as np
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorDiagnosticsProfile,
    FactorDiagnosticsKind,
    FactorScoreQuality,
    create_factor_diagnostics_profile_id,
)


def compute_factor_correlation_matrix(
    df: pd.DataFrame, factor_columns: list[str]
) -> pd.DataFrame:
    valid_cols = [c for c in factor_columns if c in df.columns]
    if len(valid_cols) < 2:
        return pd.DataFrame()
    return df[valid_cols].corr()


def high_factor_correlation_pairs(
    df: pd.DataFrame, factor_columns: list[str], threshold: float = 0.95
) -> list[dict[str, Any]]:
    corr = compute_factor_correlation_matrix(df, factor_columns)
    if corr.empty:
        return []

    mask = np.triu(np.ones(corr.shape, dtype=bool), k=1)
    upper_tri = corr.where(mask)
    stacked = upper_tri.stack()
    filtered = stacked[stacked.abs() >= threshold]

    pairs = [
        {"factor1": str(idx[0]), "factor2": str(idx[1]), "correlation": float(val)}
        for idx, val in filtered.items()
    ]
    return pairs


def build_factor_correlation_diagnostics(
    df: pd.DataFrame, factor_columns: list[str], symbol: str | None = None
) -> list[FactorDiagnosticsProfile]:
    pairs = high_factor_correlation_pairs(df, factor_columns)
    if not pairs:
        return []

    # associate warnings
    warns_by_col = {c: [] for c in factor_columns}
    for p in pairs:
        warns_by_col[p["factor1"]].append(p)
        warns_by_col[p["factor2"]].append(p)

    profiles = []
    for col, w_list in warns_by_col.items():
        if w_list:
            prof = FactorDiagnosticsProfile(
                diagnostics_id=create_factor_diagnostics_profile_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                symbol=symbol,
                factor_name=col,
                diagnostics_kinds=[
                    FactorDiagnosticsKind.CORRELATION,
                    FactorDiagnosticsKind.REDUNDANCY,
                ],
                row_count=len(df),
                coverage_ratio=0.0,
                missingness_ratio=0.0,
                finite_ratio=0.0,
                outlier_ratio=0.0,
                stability_score=0.0,
                correlation_warnings=w_list,
                redundancy_score=1.0,
                distribution_summary={},
                quality=FactorScoreQuality.WARNING,
                warnings=[f"High correlation pairs found: {len(w_list)}"],
                errors=[],
                risk_flags=[],
                metadata={},
            )
            profiles.append(prof)
    return profiles


def validate_factor_correlation_diagnostics(
    profiles: list[FactorDiagnosticsProfile],
) -> list[str]:
    return []


def factor_correlation_diagnostics_summary(
    profiles: list[FactorDiagnosticsProfile],
) -> dict[str, Any]:
    return {"status": "ok"}
