import pandas as pd
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimeDurationAnalyticsError
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeDurationProfile,
    create_regime_duration_profile_id,
    _now
)
from usa_signal_bot.regime_classification.diagnostics.regime_persistence_analytics import compute_regime_runs

def run_lengths_by_label(labels: List[str]) -> Dict[str, List[int]]:
    runs = compute_regime_runs(labels)
    by_label = {}
    for r in runs:
        lbl = r["label"]
        if lbl not in by_label:
            by_label[lbl] = []
        by_label[lbl].append(r["length"])
    return by_label

def build_duration_profiles_for_labels(labels: List[str], symbol: Optional[str] = None) -> List[RegimeDurationProfile]:
    runs_dict = run_lengths_by_label(labels)
    profiles = []
    for lbl, lengths in runs_dict.items():
        sl = sorted(lengths)
        count = len(sl)
        profiles.append(RegimeDurationProfile(
            duration_id=create_regime_duration_profile_id(),
            created_at_utc=_now(),
            symbol=symbol,
            label_name=lbl,
            run_lengths=lengths,
            run_count=count,
            min_duration=sl[0] if sl else None,
            max_duration=sl[-1] if sl else None,
            average_duration=(sum(sl) / count) if count > 0 else None,
            median_duration=(sl[count // 2] if count % 2 == 1 else (sl[count // 2 - 1] + sl[count // 2]) / 2.0) if count > 0 else None,
            latest_duration=lengths[-1] if lengths else None,
            duration_profile_valid=True,
            research_metadata_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ))
    return profiles

def build_duration_profiles_for_table(symbol: Optional[str], df: pd.DataFrame, label_column: str = "regime_label_research") -> List[RegimeDurationProfile]:
    if label_column not in df.columns:
        raise RegimeDurationAnalyticsError(f"Missing column '{label_column}'")
    labels = df[label_column].tolist()
    return build_duration_profiles_for_labels(labels, symbol)

def build_duration_profiles(tables: Dict[str, pd.DataFrame]) -> List[RegimeDurationProfile]:
    profiles = []
    for symbol, df in tables.items():
        profiles.extend(build_duration_profiles_for_table(symbol, df))
    return profiles

def validate_duration_profiles(profiles: List[RegimeDurationProfile]) -> List[str]:
    errors = []
    for p in profiles:
        if p.min_duration is not None and p.max_duration is not None:
            if p.min_duration > p.max_duration:
                errors.append(f"Invalid min/max duration for {p.label_name}")
    return errors

def duration_analytics_summary(profiles: List[RegimeDurationProfile]) -> Dict[str, Any]:
    return {"profile_count": len(profiles)}

def duration_analytics_to_text(profiles: List[RegimeDurationProfile], limit: int = 300) -> str:
    lines = ["Regime Duration Profiles"]
    for p in profiles[:limit]:
        lines.append(f"[{p.symbol or 'UNKNOWN'}] {p.label_name}: Min={p.min_duration}, Max={p.max_duration}, Avg={p.average_duration}")
    return "\n".join(lines)
