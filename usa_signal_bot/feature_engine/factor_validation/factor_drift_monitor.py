import pandas as pd
from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorDriftBaseline,
    FactorDriftReport,
    FactorDriftObservation,
    FactorDriftStatus,
    FactorDriftMetricKind,
    create_factor_drift_observation_id,
    create_factor_drift_report_id,
    validate_factor_drift_report
)
from usa_signal_bot.feature_engine.factor_validation.factor_baseline_builder import compute_factor_baseline_stats
from usa_signal_bot.feature_engine.factor_validation.factor_drift_metrics import (
    compute_mean_shift,
    compute_std_shift,
    compute_median_shift,
    drift_status_from_score
)

def build_drift_observations(symbol: str, factor_column: str, baseline_stats: dict[str, Any], observed_stats: dict[str, Any]) -> list[FactorDriftObservation]:
    obs = []
    shifts = [
        (FactorDriftMetricKind.MEAN_SHIFT, compute_mean_shift),
        (FactorDriftMetricKind.STD_SHIFT, compute_std_shift),
        (FactorDriftMetricKind.MEDIAN_SHIFT, compute_median_shift)
    ]
    for kind, func in shifts:
        shift = func(baseline_stats, observed_stats)
        score = min(shift * 100, 100.0) # dummy scaling
        obs.append(FactorDriftObservation(
            observation_id=create_factor_drift_observation_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            symbol=symbol,
            factor_column=factor_column,
            metric_kind=kind,
            baseline_value=baseline_stats.get(kind.name.split('_')[0].lower()),
            observed_value=observed_stats.get(kind.name.split('_')[0].lower()),
            absolute_change=shift,
            relative_change=shift,
            drift_score=score,
            drift_status=drift_status_from_score(score),
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return obs

def overall_drift_status(observations: list[FactorDriftObservation]) -> FactorDriftStatus:
    if not observations:
        return FactorDriftStatus.UNKNOWN
    max_score = max(o.drift_score for o in observations)
    return drift_status_from_score(max_score)

def run_factor_drift_monitor(symbol: str, baseline: FactorDriftBaseline | None, observed_df: pd.DataFrame, factor_columns: list[str] | None = None) -> FactorDriftReport:
    if factor_columns is None:
        factor_columns = [c for c in observed_df.columns if c not in ['symbol', 'timestamp', 'date', 'datetime']]

    observed_stats = compute_factor_baseline_stats(observed_df, factor_columns)

    observations = []
    if baseline and baseline.baseline_valid:
        for c in factor_columns:
            if c in baseline.baseline_stats and c in observed_stats:
                observations.extend(build_drift_observations(symbol, c, baseline.baseline_stats[c], observed_stats[c]))

    warnings = []
    if not baseline or not baseline.baseline_valid:
        warnings.append("Baseline missing")

    max_drift = max([o.drift_score for o in observations] + [0.0])
    avg_drift = sum(o.drift_score for o in observations) / len(observations) if observations else 0.0

    high_cols = list(set(o.factor_column for o in observations if o.drift_status == FactorDriftStatus.HIGH_DRIFT))
    crit_cols = list(set(o.factor_column for o in observations if o.drift_status == FactorDriftStatus.CRITICAL_DRIFT))

    report = FactorDriftReport(
        drift_report_id=create_factor_drift_report_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        baseline_id=baseline.baseline_id if baseline else None,
        observations=observations,
        overall_drift_status=overall_drift_status(observations) if baseline else FactorDriftStatus.BASELINE_MISSING,
        max_drift_score=max_drift,
        average_drift_score=avg_drift,
        high_drift_factor_columns=high_cols,
        critical_drift_factor_columns=crit_cols,
        baseline_available=bool(baseline and baseline.baseline_valid),
        drift_report_valid=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=warnings,
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_drift_report(report)
    return report

def run_factor_drift_monitor_for_tables(baselines: list[FactorDriftBaseline], observed_tables: dict[str, pd.DataFrame]) -> list[FactorDriftReport]:
    b_map = {b.symbol: b for b in baselines}
    reports = []
    for sym, df in observed_tables.items():
        reports.append(run_factor_drift_monitor(sym, b_map.get(sym), df))
    return reports

def factor_drift_monitor_summary(reports: list[FactorDriftReport]) -> dict[str, Any]:
    return {"reports_count": len(reports)}

def factor_drift_monitor_to_text(reports: list[FactorDriftReport], limit: int = 200) -> str:
    return f"Generated {len(reports)} drift reports."
