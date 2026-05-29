import pandas as pd
from typing import Any

def resolve_candidate_score_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if "score" in col.lower() and ("candidate" in col.lower() or "regime" in col.lower())]

def candidate_name_from_score_column(column: str) -> str:
    # simple heuristic: remove "score"
    name = column.lower().replace("score", "").replace("_", " ").strip()
    return name.replace(" ", "_")

def taxonomy_label_from_candidate_name(candidate_name: str) -> str:
    # mapping candidate names to taxonomy labels
    if "bull" in candidate_name or "up" in candidate_name:
        return "bull_regime"
    if "bear" in candidate_name or "down" in candidate_name:
        return "bear_regime"
    if "volatil" in candidate_name:
        if "high" in candidate_name:
            return "high_volatility"
        return "low_volatility"
    if "range" in candidate_name or "chop" in candidate_name:
        return "ranging_regime"
    return "unknown_regime"

def top_two_candidate_scores(row: pd.Series, score_columns: list[str]) -> dict[str, Any]:
    scores = [(col, row[col]) for col in score_columns if pd.notna(row[col])]
    scores.sort(key=lambda x: x[1], reverse=True)

    top = scores[0] if len(scores) > 0 else (None, None)
    second = scores[1] if len(scores) > 1 else (None, None)

    return {
        "top_column": top[0],
        "top_score": top[1],
        "second_column": second[0],
        "second_score": second[1]
    }

def candidate_score_summary_for_row(row: pd.Series, score_columns: list[str]) -> dict[str, Any]:
    top_two = top_two_candidate_scores(row, score_columns)

    top_candidate = candidate_name_from_score_column(top_two["top_column"]) if top_two["top_column"] else None
    second_candidate = candidate_name_from_score_column(top_two["second_column"]) if top_two["second_column"] else None

    gap = top_two["top_score"] - top_two["second_score"] if top_two["top_score"] is not None and top_two["second_score"] is not None else None

    return {
        "top_candidate": top_candidate,
        "top_score": top_two["top_score"],
        "second_candidate": second_candidate,
        "second_score": top_two["second_score"],
        "score_gap": gap
    }

def validate_candidate_score_columns(columns: list[str]) -> list[str]:
    errors = []
    if not columns:
        errors.append("No candidate score columns found")
    for col in columns:
        if "prediction" in col.lower() or "prob" in col.lower():
            errors.append(f"Score column suggests model prediction: {col}")
    return errors

def candidate_score_resolver_summary(df: pd.DataFrame) -> dict[str, Any]:
    cols = resolve_candidate_score_columns(df)
    return {
        "score_columns": cols,
        "count": len(cols)
    }
