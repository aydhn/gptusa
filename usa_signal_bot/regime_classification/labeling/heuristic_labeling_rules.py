import pandas as pd
from typing import Any

from usa_signal_bot.core.enums import RegimeLabelingMethod, RegimeLabelConflictKind
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeLabelingSpec,
    HeuristicRegimeLabelResult,
    create_heuristic_regime_label_result_id,
    _now_utc
)
from usa_signal_bot.regime_classification.labeling.candidate_score_resolver import (
    candidate_score_summary_for_row,
    taxonomy_label_from_candidate_name,
    resolve_candidate_score_columns
)
from usa_signal_bot.regime_classification.labeling.label_confidence_proxy import (
    compute_score_level_confidence,
    compute_score_gap_confidence,
    combine_label_confidence,
    confidence_kind_from_values
)
from usa_signal_bot.regime_classification.labeling.label_conflict_detector import detect_label_conflicts_for_result

def determine_label_from_candidate_scores(score_summary: dict[str, Any], spec: RegimeLabelingSpec) -> dict[str, Any]:
    top_score = score_summary.get("top_score")
    top_candidate = score_summary.get("top_candidate")
    gap = score_summary.get("score_gap")

    assigned_label = spec.unknown_label
    assigned_label_kind = "unknown"
    fallback_used = True
    mixed_used = False

    if top_score is not None and top_score >= spec.minimum_score_threshold:
        if gap is not None and gap >= spec.minimum_score_gap:
            if top_candidate:
                assigned_label = taxonomy_label_from_candidate_name(top_candidate)
                assigned_label_kind = "top_candidate"
                fallback_used = False
        else:
            if spec.conflict_policy == "fallback_to_mixed_or_unknown":
                assigned_label = spec.mixed_label
                assigned_label_kind = "mixed"
                mixed_used = True
                fallback_used = False

    return {
        "assigned_label": assigned_label,
        "assigned_label_kind": assigned_label_kind,
        "fallback_used": fallback_used,
        "mixed_label_used": mixed_used,
        "unknown_label_used": fallback_used and not mixed_used
    }

def detect_label_conflicts_from_scores(score_summary: dict[str, Any], spec: RegimeLabelingSpec) -> list[RegimeLabelConflictKind]:
    conflicts = []
    top = score_summary.get("top_score")
    second = score_summary.get("second_score")
    gap = score_summary.get("score_gap")

    if top is not None and top < 30.0:
        conflicts.append(RegimeLabelConflictKind.LOW_SCORE_ALL_CANDIDATES)

    if top is not None and second is not None and top > 60.0 and second > 60.0 and gap is not None and gap < 5.0:
        conflicts.append(RegimeLabelConflictKind.MULTIPLE_HIGH_SCORE_CANDIDATES)

    return conflicts

def assign_heuristic_regime_label_for_row(row: pd.Series, spec: RegimeLabelingSpec, score_columns: list[str]) -> HeuristicRegimeLabelResult:
    summary = candidate_score_summary_for_row(row, score_columns)
    label_decision = determine_label_from_candidate_scores(summary, spec)

    c_level = compute_score_level_confidence(summary.get("top_score"))
    c_gap = compute_score_gap_confidence(summary.get("top_score"), summary.get("second_score"))
    conf_score = combine_label_confidence([c_level, c_gap])

    conflicts = detect_label_conflicts_from_scores(summary, spec)
    conf_kind = confidence_kind_from_values(conf_score, len(conflicts))

    symbol = row.get("symbol")
    ts = row.get("timestamp") or row.get("date")

    result = HeuristicRegimeLabelResult(
        label_result_id=create_heuristic_regime_label_result_id(),
        created_at_utc=_now_utc(),
        symbol=str(symbol) if pd.notna(symbol) else None,
        timestamp=str(ts) if pd.notna(ts) else None,
        assigned_label=label_decision["assigned_label"],
        assigned_label_kind=label_decision["assigned_label_kind"],
        method=spec.method,
        top_candidate_name=summary.get("top_candidate"),
        top_candidate_score=summary.get("top_score"),
        second_candidate_name=summary.get("second_candidate"),
        second_candidate_score=summary.get("second_score"),
        score_gap=summary.get("score_gap"),
        confidence_score=conf_score,
        confidence_kind=conf_kind,
        conflict_kinds=conflicts,
        fallback_used=label_decision["fallback_used"],
        mixed_label_used=label_decision["mixed_label_used"],
        unknown_label_used=label_decision["unknown_label_used"],
        validation_status="NOT_CHECKED",
        research_metadata_only=True,
        model_prediction=False,
        model_training_used=False,
        activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )
    return result

def assign_heuristic_regime_labels_for_table(symbol: str | None, df: pd.DataFrame, spec: RegimeLabelingSpec | None = None) -> tuple[pd.DataFrame, list[HeuristicRegimeLabelResult]]:
    if spec is None:
        from usa_signal_bot.regime_classification.labeling.regime_labeling_specs import build_default_regime_labeling_specs
        spec = build_default_regime_labeling_specs()[0]

    score_cols = spec.candidate_score_columns
    if not score_cols:
        score_cols = resolve_candidate_score_columns(df)

    results = []
    labels = []
    methods = []
    confidences = []
    tops = []
    gaps = []
    conflicts = []
    fallbacks = []

    for _, row in df.iterrows():
        res = assign_heuristic_regime_label_for_row(row, spec, score_cols)
        if symbol and not res.symbol:
            res.symbol = symbol
        results.append(res)

        labels.append(res.assigned_label)
        methods.append(res.method.value)
        confidences.append(res.confidence_score)
        tops.append(res.top_candidate_name)
        gaps.append(res.score_gap)
        conflicts.append(len(res.conflict_kinds))
        fallbacks.append(res.fallback_used)

    out_df = df.copy()
    out_df["regime_label_research"] = labels
    out_df["regime_label_method"] = methods
    out_df["regime_label_confidence"] = confidences
    out_df["regime_label_top_candidate"] = tops
    out_df["regime_label_score_gap"] = gaps
    out_df["regime_label_conflict_count"] = conflicts
    out_df["regime_label_fallback_used"] = fallbacks

    return out_df, results

def assign_heuristic_regime_labels(tables: dict[str, pd.DataFrame], spec: RegimeLabelingSpec | None = None) -> tuple[dict[str, pd.DataFrame], list[HeuristicRegimeLabelResult]]:
    out_tables = {}
    all_results = []
    for sym, df in tables.items():
        o_df, res = assign_heuristic_regime_labels_for_table(sym, df, spec)
        out_tables[sym] = o_df
        all_results.extend(res)
    return out_tables, all_results

def validate_heuristic_label_results(results: list[HeuristicRegimeLabelResult]) -> list[str]:
    errors = []
    for r in results:
        if r.model_prediction:
            errors.append(f"Result {r.label_result_id} is marked as model prediction")
        if r.produces_trade_signal or r.produces_order_decision or r.produces_portfolio_weights:
            errors.append(f"Result {r.label_result_id} produces execution outputs")
    return errors

def heuristic_labeling_rules_summary(results: list[HeuristicRegimeLabelResult]) -> dict[str, Any]:
    counts = {}
    for r in results:
        counts[r.assigned_label] = counts.get(r.assigned_label, 0) + 1
    return {
        "total_results": len(results),
        "label_counts": counts
    }

def heuristic_labeling_rules_to_text(results: list[HeuristicRegimeLabelResult], limit: int = 200) -> str:
    summary = heuristic_labeling_rules_summary(results)
    return f"Heuristic Labels: {summary['total_results']} total. Counts: {summary['label_counts']}"
