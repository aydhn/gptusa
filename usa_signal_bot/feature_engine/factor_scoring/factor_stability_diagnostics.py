from typing import Any
import pandas as pd
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorDiagnosticsProfile,
    FactorDiagnosticsKind,
    FactorScoreQuality,
    create_factor_diagnostics_profile_id
)

def compute_factor_stability_score(series: pd.Series) -> float:
    if series.empty or series.isna().all():
        return 0.0
    finite_ratio = float(series.notna().sum() / len(series))
    if series.nunique() <= 1:
        return 0.0
    return finite_ratio * 100.0

def build_factor_stability_diagnostics(df: pd.DataFrame, factor_columns: list[str], symbol: str | None = None) -> list[FactorDiagnosticsProfile]:
    profiles = []
    for col in factor_columns:
        if col not in df.columns:
            continue
        series = df[col]
        stability = compute_factor_stability_score(series)

        prof = FactorDiagnosticsProfile(
            diagnostics_id=create_factor_diagnostics_profile_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            symbol=symbol,
            factor_name=col,
            diagnostics_kinds=[FactorDiagnosticsKind.STABILITY],
            row_count=len(series),
            coverage_ratio=0.0,
            missingness_ratio=0.0,
            finite_ratio=0.0,
            outlier_ratio=0.0,
            stability_score=stability,
            correlation_warnings=[],
            redundancy_score=0.0,
            distribution_summary={},
            quality=FactorScoreQuality.ACCEPTABLE if stability > 50.0 else FactorScoreQuality.WARNING,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        profiles.append(prof)
    return profiles

def low_stability_factor_columns(df: pd.DataFrame, factor_columns: list[str], threshold: float = 40.0) -> list[str]:
    low = []
    for col in factor_columns:
        if col in df.columns:
            if compute_factor_stability_score(df[col]) < threshold:
                low.append(col)
    return low

def validate_factor_stability_diagnostics(profiles: list[FactorDiagnosticsProfile]) -> list[str]:
    return []

def factor_stability_diagnostics_summary(profiles: list[FactorDiagnosticsProfile]) -> dict[str, Any]:
    return {"status": "ok"}
