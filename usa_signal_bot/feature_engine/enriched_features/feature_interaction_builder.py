import pandas as pd
from typing import Any
from usa_signal_bot.core.enums import FeatureInteractionKind
from usa_signal_bot.feature_engine.enriched_features.phase119_models import FeatureInteractionSpec

def add_feature_interactions(df: pd.DataFrame, specs: list[FeatureInteractionSpec] | None = None) -> pd.DataFrame:
    df = df.copy()
    if not specs:
        return df

    for spec in specs:
        if spec.left_feature not in df.columns:
            continue
        if spec.right_feature and spec.right_feature not in df.columns:
            continue
        if spec.conditioning_feature and spec.conditioning_feature not in df.columns:
            continue

        df[spec.output_column] = compute_interaction(df, spec)

    return df

def compute_interaction(df: pd.DataFrame, spec: FeatureInteractionSpec) -> pd.Series:
    if spec.interaction_kind == FeatureInteractionKind.MULTIPLICATIVE:
        return compute_multiplicative_interaction(df[spec.left_feature], df[spec.right_feature])
    elif spec.interaction_kind == FeatureInteractionKind.RATIO:
        return compute_ratio_interaction(df[spec.left_feature], df[spec.right_feature])
    elif spec.interaction_kind == FeatureInteractionKind.DIFFERENCE:
        return compute_difference_interaction(df[spec.left_feature], df[spec.right_feature])
    elif spec.interaction_kind == FeatureInteractionKind.EVENT_CONDITIONED:
        return compute_event_conditioned_interaction(df[spec.left_feature], df[spec.conditioning_feature])
    elif spec.interaction_kind == FeatureInteractionKind.QUALITY_WEIGHTED:
        return compute_multiplicative_interaction(df[spec.left_feature], df[spec.conditioning_feature])
    elif spec.interaction_kind == FeatureInteractionKind.CALENDAR_CONDITIONED:
        return compute_event_conditioned_interaction(df[spec.left_feature], df[spec.conditioning_feature])
    else:
        return pd.Series(0.0, index=df.index)

def compute_multiplicative_interaction(left: pd.Series, right: pd.Series) -> pd.Series:
    return left * right

def compute_ratio_interaction(left: pd.Series, right: pd.Series, epsilon: float = 1e-9) -> pd.Series:
    return left / (right + epsilon)

def compute_difference_interaction(left: pd.Series, right: pd.Series) -> pd.Series:
    return left - right

def compute_event_conditioned_interaction(base: pd.Series, condition: pd.Series) -> pd.Series:
    return base * condition

def validate_feature_interactions(df: pd.DataFrame) -> list[str]:
    return []

def feature_interaction_builder_summary(df: pd.DataFrame) -> dict[str, Any]:
    return {"columns": list(df.columns)}
