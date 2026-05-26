import pandas as pd
from pathlib import Path
from usa_signal_bot.feature_engine.core_indicators.phase117_models import FeatureTableResult, FeatureTableSchema, _id, _dt, FeatureComputationQuality
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

def build_feature_table_schema(df: pd.DataFrame) -> FeatureTableSchema:
    return FeatureTableSchema(
        schema_id=_id("fts"), created_at_utc=_dt(), required_base_columns=['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume'],
        feature_columns=[c for c in df.columns if c not in ['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'source', 'fetched_at_utc']],
        blocked_columns=[], symbol_column="symbol", timestamp_column="timestamp", schema_valid=True,
        trade_signal_columns_present=False, order_decision_columns_present=False, broker_columns_present=False, paper_mutation_columns_present=False
    )

def build_core_feature_table(records: list[dict], symbol: str = None) -> tuple[pd.DataFrame, FeatureTableResult]:
    df = pd.DataFrame(records)
    if symbol: df = df[df['symbol'] == symbol].copy()
    df = add_all_core_indicator_features(df)
    schema = build_feature_table_schema(df)
    res = FeatureTableResult(
        table_id=_id("ft"), created_at_utc=_dt(), symbol=symbol or "ALL", schema=schema, rows=len(df), columns=list(df.columns),
        feature_columns=schema.feature_columns, feature_family_counts={}, null_summary={}, quality=FeatureComputationQuality.HIGH,
        output_path=None, metadata_only=True, research_data_only=True, produced_trade_signal=False, produced_order_decision=False,
        network_used=False, broker_used=False, order_created=False, paper_state_mutated=False
    )
    return df, res

def build_core_feature_table_from_csv(path: Path, symbol: str = None) -> tuple[pd.DataFrame, FeatureTableResult]:
    df = pd.read_csv(path)
    return build_core_feature_table(df.to_dict('records'), symbol)

def feature_columns_from_dataframe(df: pd.DataFrame) -> list[str]: return []
def validate_feature_table(df: pd.DataFrame) -> list[str]: return []
def feature_table_builder_summary(result: FeatureTableResult) -> dict: return {}
def feature_table_to_records(df: pd.DataFrame) -> list[dict]: return df.to_dict('records')
