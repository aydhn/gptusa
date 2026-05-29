import pandas as pd
from collections import Counter
from typing import Any

from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeLabelSequence,
    create_regime_label_sequence_id,
    _now_utc
)
from usa_signal_bot.regime_classification.labeling.rolling_regime_windows import compute_label_switch_count

def count_regime_labels(labels: list[str]) -> dict[str, int]:
    valid_labels = [l for l in labels if pd.notna(l)]
    return dict(Counter(valid_labels))

def dominant_regime_label(labels: list[str]) -> tuple[str | None, float | None]:
    valid_labels = [l for l in labels if pd.notna(l)]
    if not valid_labels:
        return None, None
    c = Counter(valid_labels)
    dom, count = c.most_common(1)[0]
    return dom, count / len(valid_labels)

def average_label_confidence(confidences: list[float]) -> float | None:
    valid = [c for c in confidences if pd.notna(c)]
    if not valid:
        return None
    return sum(valid) / len(valid)

def build_regime_label_sequence(symbol: str | None, df: pd.DataFrame, label_column: str = "regime_label_research", confidence_column: str = "regime_label_confidence") -> RegimeLabelSequence:
    labels = df[label_column].tolist() if label_column in df.columns else []
    confs = df[confidence_column].tolist() if confidence_column in df.columns else []

    counts = count_regime_labels(labels)
    dom, ratio = dominant_regime_label(labels)
    avg_conf = average_label_confidence(confs)
    switches = compute_label_switch_count(labels)

    return RegimeLabelSequence(
        sequence_id=create_regime_label_sequence_id(),
        created_at_utc=_now_utc(),
        symbol=symbol,
        rows=len(df),
        label_column=label_column,
        confidence_column=confidence_column,
        labels=labels,
        label_counts=counts,
        label_switch_count=switches,
        dominant_label=dom,
        dominant_label_ratio=ratio,
        average_confidence=avg_conf,
        sequence_valid=len(labels) > 0,
        research_metadata_only=True,
        model_prediction=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_regime_label_sequences(tables: dict[str, pd.DataFrame]) -> list[RegimeLabelSequence]:
    seqs = []
    for sym, df in tables.items():
        seqs.append(build_regime_label_sequence(sym, df))
    return seqs

def validate_regime_label_sequence(sequence: RegimeLabelSequence) -> list[str]:
    errors = []
    if sequence.model_prediction:
        errors.append(f"Sequence {sequence.sequence_id} marked as model prediction")
    if sequence.produces_trade_signal or sequence.produces_order_decision or sequence.produces_portfolio_weights:
        errors.append(f"Sequence {sequence.sequence_id} produces execution outputs")
    return errors

def regime_label_sequence_summary(sequences: list[RegimeLabelSequence]) -> dict[str, Any]:
    return {
        "sequence_count": len(sequences),
        "total_rows": sum(s.rows for s in sequences)
    }

def regime_label_sequence_to_text(sequences: list[RegimeLabelSequence], limit: int = 200) -> str:
    summary = regime_label_sequence_summary(sequences)
    return f"Sequences: {summary['sequence_count']}, Total Rows: {summary['total_rows']}"
