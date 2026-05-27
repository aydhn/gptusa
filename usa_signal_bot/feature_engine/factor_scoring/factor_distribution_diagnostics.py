from typing import Any
import pandas as pd
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorDiagnosticsProfile,
    FactorDiagnosticsKind,
    FactorScoreQuality,
    create_factor_diagnostics_profile_id
)

def build_factor_distribution_summary(series: pd.Series) -> dict[str, Any]:
    if series.empty or series.isna().all():
        return {}
    return {
        "count": len(series),
        "finite_count": int(series.notna().sum()),
        "null_count": int(series.isna().sum()),
        "mean": float(series.mean()),
        "std": float(series.std()),
        "min": float(series.min()),
        "max": float(series.max()),
        "median": float(series.median()),
        "q05": float(series.quantile(0.05)),
        "q25": float(series.quantile(0.25)),
        "q75": float(series.quantile(0.75)),
        "q95": float(series.quantile(0.95))
    }

def compute_outlier_ratio(series: pd.Series, z_threshold: float = 4.0) -> float:
    if series.empty or series.isna().all():
        return 0.0
    mean = series.mean()
    std = series.std()
    if pd.isna(std) or std == 0:
        return 0.0
    z = (series - mean).abs() / std
    outliers = z > z_threshold
    return float(outliers.sum() / len(series))

def build_factor_distribution_diagnostics(df: pd.DataFrame, factor_columns: list[str], symbol: str | None = None) -> list[FactorDiagnosticsProfile]:
    profiles = []
    for col in factor_columns:
        if col not in df.columns:
            continue
        series = df[col]
        row_count = len(series)
        null_count = int(series.isna().sum())
        finite_count = row_count - null_count

        coverage_ratio = finite_count / row_count if row_count > 0 else 0.0
        missingness_ratio = null_count / row_count if row_count > 0 else 1.0
        finite_ratio = coverage_ratio
        outlier_ratio = compute_outlier_ratio(series)

        quality = FactorScoreQuality.ACCEPTABLE
        if coverage_ratio < 0.5:
            quality = FactorScoreQuality.WARNING

        prof = FactorDiagnosticsProfile(
            diagnostics_id=create_factor_diagnostics_profile_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            symbol=symbol,
            factor_name=col,
            diagnostics_kinds=[FactorDiagnosticsKind.COVERAGE, FactorDiagnosticsKind.MISSINGNESS, FactorDiagnosticsKind.DISTRIBUTION, FactorDiagnosticsKind.OUTLIER],
            row_count=row_count,
            coverage_ratio=coverage_ratio,
            missingness_ratio=missingness_ratio,
            finite_ratio=finite_ratio,
            outlier_ratio=outlier_ratio,
            stability_score=0.0,
            correlation_warnings=[],
            redundancy_score=0.0,
            distribution_summary=build_factor_distribution_summary(series),
            quality=quality,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        profiles.append(prof)
    return profiles

def validate_factor_distribution_diagnostics(profiles: list[FactorDiagnosticsProfile]) -> list[str]:
    return []

def factor_distribution_diagnostics_summary(profiles: list[FactorDiagnosticsProfile]) -> dict[str, Any]:
    return {"status": "ok"}
