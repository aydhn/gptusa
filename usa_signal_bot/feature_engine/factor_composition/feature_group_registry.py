from typing import Any
from usa_signal_bot.core.enums import FeatureGroupKind
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureGroupDefinition,
    create_feature_group_definition_id,
    validate_feature_group_definition,
    _now_str
)

def build_default_feature_group_definitions(columns: list[str] | None = None) -> list[FeatureGroupDefinition]:
    groups = []

    group_configs = [
        ("price_action", FeatureGroupKind.PRICE_ACTION, "Base price action indicators"),
        ("returns", FeatureGroupKind.RETURNS, "Log and simple return streams"),
        ("volatility", FeatureGroupKind.VOLATILITY, "Volatility and ATR metrics"),
        ("momentum", FeatureGroupKind.MOMENTUM, "Momentum oscillators and derivatives"),
        ("trend", FeatureGroupKind.TREND, "Moving average and trend metrics"),
        ("volume_liquidity", FeatureGroupKind.VOLUME_LIQUIDITY, "Volume and liquidity features"),
        ("cross_sectional", FeatureGroupKind.CROSS_SECTIONAL, "Cross sectional rankings"),
        ("event_context", FeatureGroupKind.EVENT_CONTEXT, "Event aware features"),
        ("quality_context", FeatureGroupKind.QUALITY_CONTEXT, "Quality aware features"),
        ("calendar_context", FeatureGroupKind.CALENDAR_CONTEXT, "Calendar aware features"),
        ("confidence_freshness", FeatureGroupKind.CONFIDENCE_FRESHNESS, "Data confidence and freshness metrics"),
        ("interactions", FeatureGroupKind.INTERACTIONS, "Feature interactions"),
        ("lineage_context", FeatureGroupKind.LINEAGE_CONTEXT, "Data lineage tracking")
    ]

    for name, kind, desc in group_configs:
        group = FeatureGroupDefinition(
            group_id=create_feature_group_definition_id(),
            created_at_utc=_now_str(),
            group_name=name,
            group_kind=kind,
            required=True,
            description=desc,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False
        )
        groups.append(group)

    if columns:
        groups = assign_columns_to_feature_groups(columns, groups)

    return groups

def feature_group_by_name(name: str, groups: list[FeatureGroupDefinition] | None = None) -> FeatureGroupDefinition | None:
    if not groups: return None
    for g in groups:
        if g.group_name == name:
            return g
    return None

def infer_feature_group_kind(column_name: str) -> FeatureGroupKind:
    col = column_name.lower()
    if "return" in col: return FeatureGroupKind.RETURNS
    if "volatility" in col or "atr" in col or "std" in col: return FeatureGroupKind.VOLATILITY
    if "momentum" in col or "rsi" in col or "macd" in col or "stoch" in col: return FeatureGroupKind.MOMENTUM
    if "trend" in col or "ma" in col or "ema" in col or "sma" in col: return FeatureGroupKind.TREND
    if "vol" in col or "liquidity" in col or "turnover" in col: return FeatureGroupKind.VOLUME_LIQUIDITY
    if "cross" in col or "rank" in col or "sector" in col: return FeatureGroupKind.CROSS_SECTIONAL
    if "event" in col or "earnings" in col or "macro" in col: return FeatureGroupKind.EVENT_CONTEXT
    if "quality" in col or "fundamental" in col: return FeatureGroupKind.QUALITY_CONTEXT
    if "calendar" in col or "hour" in col or "day" in col or "month" in col: return FeatureGroupKind.CALENDAR_CONTEXT
    if "confidence" in col or "freshness" in col: return FeatureGroupKind.CONFIDENCE_FRESHNESS
    if "interaction" in col or "_x_" in col or "_div_" in col: return FeatureGroupKind.INTERACTIONS
    if "lineage" in col: return FeatureGroupKind.LINEAGE_CONTEXT
    return FeatureGroupKind.PRICE_ACTION

def assign_columns_to_feature_groups(columns: list[str], groups: list[FeatureGroupDefinition] = None) -> list[FeatureGroupDefinition]:
    if not groups:
        groups = build_default_feature_group_definitions()

    for col in columns:
        if col in ['symbol', 'timestamp']:
            continue
        kind = infer_feature_group_kind(col)
        for g in groups:
            if g.group_kind == kind:
                if col not in g.feature_columns:
                    g.feature_columns.append(col)
                break
    return groups

def validate_feature_group_definitions(groups: list[FeatureGroupDefinition]) -> list[str]:
    errors = []
    for g in groups:
        validate_feature_group_definition(g)
        if g.errors:
            errors.extend([f"Group {g.group_name} error: {e}" for e in g.errors])
    return errors

def feature_group_registry_summary(groups: list[FeatureGroupDefinition]) -> dict[str, Any]:
    return {
        "group_count": len(groups),
        "total_assigned_columns": sum(len(g.feature_columns) for g in groups),
        "group_names": [g.group_name for g in groups],
        "column_counts": {g.group_name: len(g.feature_columns) for g in groups}
    }

def feature_group_registry_to_text(groups: list[FeatureGroupDefinition], limit: int = 200) -> str:
    summary = feature_group_registry_summary(groups)
    lines = [
        f"Feature Group Registry: {summary['group_count']} groups",
        f"Total assigned columns: {summary['total_assigned_columns']}"
    ]
    for g in groups[:limit]:
        lines.append(f"  - {g.group_name} ({g.group_kind.value}): {len(g.feature_columns)} features")
    return "\n".join(lines)
