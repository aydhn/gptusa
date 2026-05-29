import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimePersistenceAnalyticsError
from usa_signal_bot.core.enums import RegimeDiagnosticsQuality
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimePersistenceProfile,
    create_regime_persistence_profile_id,
    _now
)

def compute_regime_runs(labels: List[str]) -> List[Dict[str, Any]]:
    runs = []
    if not labels:
        return runs

    current_label = labels[0]
    current_len = 1

    for lbl in labels[1:]:
        if pd.isna(lbl):
            continue
        if lbl == current_label:
            current_len += 1
        else:
            runs.append({"label": str(current_label), "length": current_len})
            current_label = lbl
            current_len = 1

    if not pd.isna(current_label):
        runs.append({"label": str(current_label), "length": current_len})

    return runs

def build_persistence_profiles_for_labels(labels: List[str], confidences: Optional[List[float]] = None, symbol: Optional[str] = None) -> List[RegimePersistenceProfile]:
    runs = compute_regime_runs(labels)
    valid_labels = [str(L) for L in labels if not pd.isna(L)]
    total_periods = len(valid_labels)

    if total_periods == 0:
        return []

    label_run_map = {}
    for r in runs:
        lbl = r["label"]
        if lbl not in label_run_map:
            label_run_map[lbl] = []
        label_run_map[lbl].append(r["length"])

    profiles = []
    for lbl, lengths in label_run_map.items():
        run_count = len(lengths)
        lbl_total = sum(lengths)
        avg_len = lbl_total / run_count if run_count > 0 else 0.0
        sorted_lens = sorted(lengths)
        med_len = sorted_lens[run_count // 2] if run_count % 2 == 1 else (sorted_lens[run_count // 2 - 1] + sorted_lens[run_count // 2]) / 2.0
        max_len = sorted_lens[-1] if sorted_lens else 0

        # Self transition rate for this label specifically
        self_trans = sum(length - 1 for length in lengths)
        total_possible = sum(length for length in lengths)
        self_rate = self_trans / total_possible if total_possible > 0 else 0.0

        avg_conf = None
        if confidences:
            lbl_confs = [c for l, c in zip(labels, confidences) if l == lbl and not pd.isna(c)]
            if lbl_confs:
                avg_conf = sum(lbl_confs) / len(lbl_confs)

        profiles.append(RegimePersistenceProfile(
            persistence_id=create_regime_persistence_profile_id(),
            created_at_utc=_now(),
            symbol=symbol,
            label_name=lbl,
            run_count=run_count,
            total_periods=lbl_total,
            average_run_length=avg_len,
            median_run_length=med_len,
            max_run_length=max_len,
            persistence_ratio=(lbl_total / total_periods) if total_periods > 0 else 0.0,
            self_transition_rate=self_rate,
            average_confidence=avg_conf,
            quality=RegimeDiagnosticsQuality.HIGH,
            research_metadata_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ))
    return profiles

def build_persistence_profiles_for_table(symbol: Optional[str], df: pd.DataFrame, label_column: str = "regime_label_research", confidence_column: str = "regime_label_confidence") -> List[RegimePersistenceProfile]:
    if label_column not in df.columns:
        raise RegimePersistenceAnalyticsError(f"Label column '{label_column}' not found.")
    labels = df[label_column].tolist()
    confidences = df[confidence_column].tolist() if confidence_column in df.columns else None
    return build_persistence_profiles_for_labels(labels, confidences, symbol)

def build_persistence_profiles(tables: Dict[str, pd.DataFrame]) -> List[RegimePersistenceProfile]:
    profiles = []
    for symbol, df in tables.items():
        profiles.extend(build_persistence_profiles_for_table(symbol, df))
    return profiles

def validate_persistence_profiles(profiles: List[RegimePersistenceProfile]) -> List[str]:
    errors = []
    for p in profiles:
        if p.persistence_ratio is not None and (p.persistence_ratio < 0 or p.persistence_ratio > 1):
            errors.append(f"Invalid persistence ratio {p.persistence_ratio} for {p.label_name}")
        if p.self_transition_rate is not None and (p.self_transition_rate < 0 or p.self_transition_rate > 1):
            errors.append(f"Invalid self transition rate {p.self_transition_rate} for {p.label_name}")
    return errors

def persistence_analytics_summary(profiles: List[RegimePersistenceProfile]) -> Dict[str, Any]:
    return {
        "profile_count": len(profiles),
        "total_runs": sum(p.run_count for p in profiles)
    }

def persistence_analytics_to_text(profiles: List[RegimePersistenceProfile], limit: int = 300) -> str:
    lines = ["Regime Persistence Profiles"]
    for p in profiles[:limit]:
        lines.append(f"[{p.symbol or 'UNKNOWN'}] {p.label_name}: AvgRun={p.average_run_length:.1f}, MaxRun={p.max_run_length}, Ratio={p.persistence_ratio:.2f}")
    return "\n".join(lines)
