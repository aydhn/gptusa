import pandas as pd
from typing import Any

from usa_signal_bot.core.enums import RegimeLabelingQuality
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeLabelStabilityProfile,
    create_regime_label_stability_profile_id,
    _now_utc
)
from usa_signal_bot.regime_classification.labeling.rolling_regime_windows import (
    compute_label_switch_count,
    compute_label_stability_score
)
from usa_signal_bot.regime_classification.labeling.regime_label_sequence import dominant_regime_label

def compute_average_run_length(labels: list[str]) -> float | None:
    valid_labels = [l for l in labels if pd.notna(l)]
    if not valid_labels:
        return None
    switches = compute_label_switch_count(valid_labels)
    # Number of runs = switches + 1
    runs = switches + 1
    return len(valid_labels) / runs

def count_low_confidence_labels(confidences: list[float], threshold: float = 40.0) -> int:
    valid_confs = [c for c in confidences if pd.notna(c)]
    return sum(1 for c in valid_confs if c < threshold)

def compute_regime_label_stability_score(labels: list[str], confidences: list[float] | None = None, conflict_count: int = 0) -> float:
    base = compute_label_stability_score(labels, confidences)
    if conflict_count > 0:
        base = max(0.0, base - (conflict_count * 0.1))
    return base

def build_regime_label_stability_profile(symbol: str | None, df: pd.DataFrame, label_column: str = "regime_label_research", confidence_column: str = "regime_label_confidence") -> RegimeLabelStabilityProfile:
    labels = df[label_column].tolist() if label_column in df.columns else []
    confs = df[confidence_column].tolist() if confidence_column in df.columns else []

    valid_labels = [l for l in labels if pd.notna(l)]
    valid_confs = [c for c in confidences if pd.notna(c)]

    switches = compute_label_switch_count(labels)
    avg_run = compute_average_run_length(labels)
    dom, dom_ratio = dominant_regime_label(labels)
    avg_conf = sum(valid_confs) / len(valid_confs) if valid_confs else None

    low_confs = count_low_confidence_labels(confs)
    conflicts = df["regime_label_conflict_count"].sum() if "regime_label_conflict_count" in df.columns else 0

    score = compute_regime_label_stability_score(labels, confidences, conflicts)

    quality = RegimeLabelingQuality.ACCEPTABLE
    if score > 80.0:
        quality = RegimeLabelingQuality.HIGH
    elif score < 40.0:
        quality = RegimeLabelingQuality.LOW

    return RegimeLabelStabilityProfile(
        stability_id=create_regime_label_stability_profile_id(),
        created_at_utc=_now_utc(),
        symbol=symbol,
        label_column=label_column,
        row_count=len(df),
        label_switch_count=switches,
        average_run_length=avg_run,
        dominant_label=dom,
        dominant_label_ratio=dom_ratio,
        average_confidence=avg_conf,
        low_confidence_count=low_confs,
        conflict_count=conflicts,
        stability_score=score,
        quality=quality,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_regime_label_stability_profiles(tables: dict[str, pd.DataFrame]) -> list[RegimeLabelStabilityProfile]:
    profiles = []
    for sym, df in tables.items():
        profiles.append(build_regime_label_stability_profile(sym, df))
    return profiles

def validate_regime_label_stability_profiles(profiles: list[RegimeLabelStabilityProfile]) -> list[str]:
    errors = []
    for p in profiles:
        if p.produces_trade_signal or p.produces_order_decision or p.produces_portfolio_weights:
            errors.append(f"Profile {p.stability_id} produces execution outputs")
    return errors

def label_stability_profiler_summary(profiles: list[RegimeLabelStabilityProfile]) -> dict[str, Any]:
    avg_score = sum(p.stability_score for p in profiles) / len(profiles) if profiles else 0.0
    return {
        "profile_count": len(profiles),
        "average_stability_score": avg_score
    }

def label_stability_profiler_to_text(profiles: list[RegimeLabelStabilityProfile], limit: int = 200) -> str:
    summary = label_stability_profiler_summary(profiles)
    return f"Stability Profiles: {summary['profile_count']}, Avg Score: {summary['average_stability_score']:.2f}"
