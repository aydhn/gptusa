import pandas as pd
from typing import List, Tuple, Dict, Any, Optional
from pathlib import Path
from usa_signal_bot.feature_engine.core_indicators.phase117_models import FeatureTableSchema, FeatureTableResult, create_feature_table_schema_id, create_feature_table_id
from usa_signal_bot.core.enums import FeatureComputationQuality
from usa_signal_bot.feature_engine.core_indicators.return_features import add_daily_return_features, add_rolling_return_features
from usa_signal_bot.feature_engine.core_indicators.moving_average_features import add_moving_average_features
from usa_signal_bot.feature_engine.core_indicators.volatility_features import add_rolling_volatility_features, add_price_range_volatility_features
from usa_signal_bot.feature_engine.core_indicators.true_range_atr_features import add_true_range_atr_features
from usa_signal_bot.feature_engine.core_indicators.rsi_features import add_rsi_features
from usa_signal_bot.feature_engine.core_indicators.macd_features import add_macd_features
from usa_signal_bot.feature_engine.core_indicators.stochastic_features import add_stochastic_features
from usa_signal_bot.feature_engine.core_indicators.bollinger_features import add_bollinger_features
from usa_signal_bot.feature_engine.core_indicators.volume_features import add_volume_features
from usa_signal_bot.feature_engine.core_indicators.price_action_features import add_price_action_features
from usa_signal_bot.feature_engine.core_indicators.gap_range_candle_features import add_gap_range_candle_features

def add_all_core_indicator_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_daily_return_features(df)
    df = add_rolling_return_features(df)
    df = add_moving_average_features(df)
    df = add_rolling_volatility_features(df)
    df = add_price_range_volatility_features(df)
    df = add_true_range_atr_features(df)
    df = add_rsi_features(df)
    df = add_macd_features(df)
    df = add_stochastic_features(df)
    df = add_bollinger_features(df)
    df = add_volume_features(df)
    df = add_price_action_features(df)
    df = add_gap_range_candle_features(df)
    return df

def feature_columns_from_dataframe(df: pd.DataFrame) -> List[str]:
    base = ["symbol", "timestamp", "open", "high", "low", "close", "adjusted_close", "volume", "source", "fetched_at_utc", "quality_flags"]
    return [c for c in df.columns if c not in base]

def build_feature_table_schema(df: pd.DataFrame) -> FeatureTableSchema:
    base = ["symbol", "timestamp", "open", "high", "low", "close", "adjusted_close", "volume"]
    fc = feature_columns_from_dataframe(df)
    blocked = [c for c in fc if "buy" in c.lower() or ("signal" in c.lower() and c.lower() != "macd_signal_9")]
    return FeatureTableSchema(
        schema_id=create_feature_table_schema_id(), created_at_utc="",
        required_base_columns=base, feature_columns=fc, blocked_columns=blocked,
        symbol_column="symbol", timestamp_column="timestamp",
        schema_valid=len(blocked) == 0,
        trade_signal_columns_present=len(blocked) > 0,
        order_decision_columns_present=len(blocked) > 0,
        broker_columns_present=False, paper_mutation_columns_present=False
    )

def build_core_feature_table(records: List[Dict[str, Any]], symbol: Optional[str] = None) -> Tuple[pd.DataFrame, FeatureTableResult]:
    df = pd.DataFrame(records)
    df_feat = add_all_core_indicator_features(df)
    schema = build_feature_table_schema(df_feat)
    res = FeatureTableResult(
        table_id=create_feature_table_id(), created_at_utc="", symbol=symbol or "UNKNOWN",
        schema=schema, rows=len(df_feat), columns=list(df_feat.columns),
        feature_columns=schema.feature_columns, feature_family_counts={},
        null_summary={}, quality=FeatureComputationQuality.HIGH if schema.schema_valid else FeatureComputationQuality.INVALID,
        output_path=None, metadata_only=False, research_data_only=True,
        produced_trade_signal=schema.trade_signal_columns_present,
        produced_order_decision=schema.order_decision_columns_present,
        network_used=False, broker_used=False, order_created=False, paper_state_mutated=False
    )
    return df_feat, res

def validate_feature_table(df: pd.DataFrame) -> List[str]:
    schema = build_feature_table_schema(df)
    errors = schema.errors.copy()
    if schema.blocked_columns:
        errors.append(f"Blocked columns found: {schema.blocked_columns}")
    return errors

def build_core_feature_table_from_csv(path: Path, symbol: Optional[str] = None) -> Tuple[pd.DataFrame, FeatureTableResult]:
    df = pd.read_csv(path)
    return build_core_feature_table(df.to_dict(orient="records"), symbol)
