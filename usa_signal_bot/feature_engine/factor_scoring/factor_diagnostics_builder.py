from typing import Any
import pandas as pd
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorDiagnosticsProfile,
    FactorScoreQuality,
    create_factor_diagnostics_profile_id
)
from usa_signal_bot.feature_engine.factor_scoring.factor_distribution_diagnostics import build_factor_distribution_diagnostics
from usa_signal_bot.feature_engine.factor_scoring.factor_correlation_diagnostics import build_factor_correlation_diagnostics
from usa_signal_bot.feature_engine.factor_scoring.factor_stability_diagnostics import build_factor_stability_diagnostics

def merge_factor_diagnostics(profiles: list[FactorDiagnosticsProfile]) -> list[FactorDiagnosticsProfile]:
    if not profiles:
        return []

    by_factor_symbol = {}
    for p in profiles:
        key = (p.factor_name, p.symbol)
        if key not in by_factor_symbol:
            by_factor_symbol[key] = []
        by_factor_symbol[key].append(p)

    merged = []
    for key, group in by_factor_symbol.items():
        if not group:
            continue

        base = group[0]
        kinds = set(base.diagnostics_kinds)
        warns = list(base.warnings)
        corr_warns = list(base.correlation_warnings)

        for p in group[1:]:
            kinds.update(p.diagnostics_kinds)
            warns.extend(p.warnings)
            corr_warns.extend(p.correlation_warnings)
            if p.stability_score > 0:
                base.stability_score = p.stability_score
            if p.redundancy_score > 0:
                base.redundancy_score = p.redundancy_score
            if p.distribution_summary:
                base.distribution_summary = p.distribution_summary
            if p.coverage_ratio > 0:
                base.coverage_ratio = p.coverage_ratio
            if p.missingness_ratio > 0:
                base.missingness_ratio = p.missingness_ratio
            if p.finite_ratio > 0:
                base.finite_ratio = p.finite_ratio
            if p.outlier_ratio > 0:
                base.outlier_ratio = p.outlier_ratio

        q = FactorScoreQuality.ACCEPTABLE
        if any(p.quality == FactorScoreQuality.WARNING for p in group):
            q = FactorScoreQuality.WARNING

        base.diagnostics_kinds = list(kinds)
        base.warnings = warns
        base.correlation_warnings = corr_warns
        base.quality = q

        merged.append(base)
    return merged

def build_factor_diagnostics(df: pd.DataFrame, factor_columns: list[str], symbol: str | None = None) -> list[FactorDiagnosticsProfile]:
    dist = build_factor_distribution_diagnostics(df, factor_columns, symbol)
    corr = build_factor_correlation_diagnostics(df, factor_columns, symbol)
    stab = build_factor_stability_diagnostics(df, factor_columns, symbol)

    all_profs = dist + corr + stab
    return merge_factor_diagnostics(all_profs)

def factor_diagnostics_quality(profiles: list[FactorDiagnosticsProfile]) -> FactorScoreQuality:
    if not profiles:
        return FactorScoreQuality.UNKNOWN
    if any(p.quality == FactorScoreQuality.WARNING for p in profiles):
        return FactorScoreQuality.WARNING
    return FactorScoreQuality.ACCEPTABLE

def validate_factor_diagnostics(profiles: list[FactorDiagnosticsProfile]) -> list[str]:
    return []

def factor_diagnostics_builder_summary(profiles: list[FactorDiagnosticsProfile]) -> dict[str, Any]:
    return {"status": "ok"}

def factor_diagnostics_builder_to_text(profiles: list[FactorDiagnosticsProfile], limit: int = 200) -> str:
    return f"Built {len(profiles)} diagnostics profiles."
