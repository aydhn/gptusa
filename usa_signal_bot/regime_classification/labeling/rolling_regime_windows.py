import pandas as pd
from typing import Any
from collections import Counter

from usa_signal_bot.core.enums import RegimeWindowKind, RegimeLabelingMethod
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RollingRegimeWindowSpec,
    RollingRegimeWindowResult,
    create_rolling_regime_window_spec_id,
    create_rolling_regime_window_result_id,
    _now_utc
)

def build_default_rolling_regime_window_specs() -> list[RollingRegimeWindowSpec]:
    specs = []

    s20 = RollingRegimeWindowSpec(
        window_spec_id=create_rolling_regime_window_spec_id(),
        created_at_utc=_now_utc(),
        window_name="short_regime_window_20",
        window_kind=RegimeWindowKind.SHORT_TERM,
        window_size=20,
        min_periods=10,
        label_column="regime_label_research",
        confidence_column="regime_label_confidence",
        output_label_column="regime_label_roll20",
        output_confidence_column="regime_confidence_roll20",
        method=RegimeLabelingMethod.ROLLING_WINDOW_MAJORITY,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

    s60 = RollingRegimeWindowSpec(
        window_spec_id=create_rolling_regime_window_spec_id(),
        created_at_utc=_now_utc(),
        window_name="medium_regime_window_60",
        window_kind=RegimeWindowKind.MEDIUM_TERM,
        window_size=60,
        min_periods=30,
        label_column="regime_label_research",
        confidence_column="regime_label_confidence",
        output_label_column="regime_label_roll60",
        output_confidence_column="regime_confidence_roll60",
        method=RegimeLabelingMethod.ROLLING_WINDOW_MAJORITY,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

    s120 = RollingRegimeWindowSpec(
        window_spec_id=create_rolling_regime_window_spec_id(),
        created_at_utc=_now_utc(),
        window_name="long_regime_window_120",
        window_kind=RegimeWindowKind.LONG_TERM,
        window_size=120,
        min_periods=60,
        label_column="regime_label_research",
        confidence_column="regime_label_confidence",
        output_label_column="regime_label_roll120",
        output_confidence_column="regime_confidence_roll120",
        method=RegimeLabelingMethod.ROLLING_WINDOW_MAJORITY,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

    specs.extend([s20, s60, s120])
    return specs

def rolling_majority_label(labels: list[str], unknown_label: str = "unknown_regime") -> str:
    valid_labels = [l for l in labels if pd.notna(l)]
    if len(valid_labels) == 0:
        return unknown_label
    c = Counter(valid_labels)
    # most common returns a list of tuples
    return c.most_common(1)[0][0]

def rolling_average_confidence(values: pd.Series, window: int, min_periods: int) -> pd.Series:
    return values.rolling(window=window, min_periods=min_periods).mean()

def compute_label_switch_count(labels: list[str]) -> int:
    valid_labels = [l for l in labels if pd.notna(l)]
    if len(valid_labels) < 2:
        return 0
    switches = sum(1 for i in range(1, len(valid_labels)) if valid_labels[i] != valid_labels[i-1])
    return switches

def compute_label_stability_score(labels: list[str], confidences: list[float] | None = None) -> float:
    valid_labels = [l for l in labels if pd.notna(l)]
    n = len(valid_labels)
    if n < 2:
        return 0.0

    switches = compute_label_switch_count(valid_labels)
    switch_rate = switches / (n - 1)

    # Simple proxy: 100 - (switch_rate * 200)
    stability = 100.0 - (switch_rate * 200.0)
    stability = max(0.0, min(100.0, stability))

    if confidences:
        valid_confs = [c for c in confidences if pd.notna(c)]
        if valid_confs:
            avg_conf = sum(valid_confs) / len(valid_confs)
            stability = (stability * 0.7) + (avg_conf * 0.3)

    return stability

def add_rolling_regime_windows_for_table(symbol: str | None, df: pd.DataFrame, specs: list[RollingRegimeWindowSpec] | None = None) -> tuple[pd.DataFrame, list[RollingRegimeWindowResult]]:
    if not specs:
        specs = build_default_rolling_regime_window_specs()

    out_df = df.copy()
    results = []

    for s in specs:
        if s.label_column not in out_df.columns:
            continue

        labels = out_df[s.label_column].tolist()

        # custom rolling apply for string labels
        roll_labels = []
        for i in range(len(labels)):
            start_idx = max(0, i - s.window_size + 1)
            window_slice = labels[start_idx:i+1]
            if len(window_slice) >= s.min_periods:
                roll_labels.append(rolling_majority_label(window_slice))
            else:
                roll_labels.append(None)

        out_df[s.output_label_column] = roll_labels

        if s.confidence_column in out_df.columns:
            out_df[s.output_confidence_column] = rolling_average_confidence(out_df[s.confidence_column], s.window_size, s.min_periods)
            avg_conf = out_df[s.output_confidence_column].mean()
        else:
            avg_conf = None

        # Overall sequence stats
        valid_labels = [l for l in roll_labels if pd.notna(l)]
        if valid_labels:
            c = Counter(valid_labels)
            dom_label = c.most_common(1)[0][0]
            dom_ratio = c.most_common(1)[0][1] / len(valid_labels)
            switches = compute_label_switch_count(valid_labels)
            stab_score = compute_label_stability_score(valid_labels)
        else:
            dom_label = None
            dom_ratio = None
            switches = 0
            stab_score = 0.0

        res = RollingRegimeWindowResult(
            window_result_id=create_rolling_regime_window_result_id(),
            created_at_utc=_now_utc(),
            symbol=symbol,
            window_name=s.window_name,
            window_kind=s.window_kind,
            window_size=s.window_size,
            row_count=len(df),
            output_label_column=s.output_label_column,
            output_confidence_column=s.output_confidence_column,
            dominant_label=dom_label,
            dominant_label_ratio=dom_ratio,
            average_confidence=avg_conf,
            label_switch_count=switches,
            stability_score=stab_score,
            research_metadata_only=True,
            model_prediction=False,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False
        )
        results.append(res)

    return out_df, results

def add_rolling_regime_windows(tables: dict[str, pd.DataFrame], specs: list[RollingRegimeWindowSpec] | None = None) -> tuple[dict[str, pd.DataFrame], list[RollingRegimeWindowResult]]:
    out_tables = {}
    all_results = []
    for sym, df in tables.items():
        o_df, res = add_rolling_regime_windows_for_table(sym, df, specs)
        out_tables[sym] = o_df
        all_results.extend(res)
    return out_tables, all_results

def validate_rolling_regime_window_results(results: list[RollingRegimeWindowResult]) -> list[str]:
    errors = []
    for r in results:
        if r.model_prediction:
            errors.append(f"Result {r.window_result_id} is marked as model prediction")
        if r.produces_trade_signal or r.produces_order_decision or r.produces_portfolio_weights:
            errors.append(f"Result {r.window_result_id} produces execution outputs")
    return errors

def rolling_regime_windows_summary(results: list[RollingRegimeWindowResult]) -> dict[str, Any]:
    return {
        "result_count": len(results),
        "windows": list(set(r.window_name for r in results))
    }
