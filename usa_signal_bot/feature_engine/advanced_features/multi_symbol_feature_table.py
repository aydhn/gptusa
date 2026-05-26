import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

from usa_signal_bot.feature_engine.advanced_features.advanced_volatility_features import add_advanced_volatility_features
from usa_signal_bot.feature_engine.advanced_features.advanced_momentum_features import add_advanced_momentum_features
from usa_signal_bot.feature_engine.advanced_features.advanced_trend_features import add_advanced_trend_features
from usa_signal_bot.feature_engine.advanced_features.normalization_features import add_normalization_features
from usa_signal_bot.feature_engine.advanced_features.cross_sectional_alignment import load_symbol_feature_tables, align_feature_tables_by_timestamp
from usa_signal_bot.feature_engine.advanced_features.cross_sectional_features import add_cross_sectional_rank_features
from usa_signal_bot.feature_engine.advanced_features.relative_strength_features import add_relative_strength_vs_benchmark
from usa_signal_bot.feature_engine.advanced_features.volatility_liquidity_ranks import add_volatility_liquidity_rank_features
from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    AdvancedFeatureTableResult,
    AdvancedFeatureComputationResult,
    create_advanced_feature_table_id,
    create_advanced_feature_result_id,
    AdvancedFeatureQuality,
    NormalizationResult
)
import datetime

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_advanced_features_for_table(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[NormalizationResult]]:
    """Generates all single-symbol advanced features."""
    df_out = df.copy()

    df_out = add_advanced_volatility_features(df_out)
    df_out = add_advanced_momentum_features(df_out)
    df_out = add_advanced_trend_features(df_out)

    # Run some default normalizations
    cols_to_norm = ["ret_1d", "close", "momentum_20"]
    df_out, norm_results = add_normalization_features(df_out, columns=[c for c in cols_to_norm if c in df_out.columns])

    return df_out, norm_results

def advanced_feature_columns_from_dataframe(df: pd.DataFrame) -> List[str]:
    # Anything not like standard OHLCV or simple math.
    # For now, just return everything that looks like our features.
    keywords = ["vol_", "atr_", "momentum_", "rsi_", "macd_", "trend_", "zscore", "percentile", "rs_", "cs_"]
    return [c for c in df.columns if any(k in c for k in keywords)]

def build_advanced_feature_table_result(symbol: str, df: pd.DataFrame, output_path: Optional[str] = None) -> AdvancedFeatureTableResult:
    adv_cols = advanced_feature_columns_from_dataframe(df)
    cs_cols = [c for c in adv_cols if c.startswith("cs_") or c.startswith("rs_")]

    null_sum = df[adv_cols].isna().sum().to_dict() if adv_cols else {}

    return AdvancedFeatureTableResult(
        table_id=create_advanced_feature_table_id(),
        created_at_utc=_now(),
        symbol=symbol,
        rows=len(df),
        columns=list(df.columns),
        advanced_feature_columns=adv_cols,
        cross_sectional_columns=cs_cols,
        feature_family_counts={},
        null_summary=null_sum,
        quality=AdvancedFeatureQuality.HIGH,
        output_path=output_path,
        metadata_only=False,
        research_data_only=True,
        produced_trade_signal=False,
        produced_order_decision=False,
        produced_portfolio_weights=False,
        network_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_multi_symbol_advanced_feature_tables(paths: Dict[str, Path], benchmark_symbol: str = "SPY") -> Tuple[Dict[str, pd.DataFrame], AdvancedFeatureComputationResult]:

    tables = load_symbol_feature_tables(paths)

    input_rows = {s: len(t) for s, t in tables.items()}

    # 1. Align
    aligned_tables, align_result = align_feature_tables_by_timestamp(tables)

    all_norm_results = []
    # 2. Single-symbol features
    for sym, df in aligned_tables.items():
        df_adv, norm_res = build_advanced_features_for_table(df)
        aligned_tables[sym] = df_adv
        all_norm_results.extend(norm_res)

    # 3. Cross-sectional features
    aligned_tables = add_cross_sectional_rank_features(aligned_tables, columns=["ret_1d", "momentum_20"])
    aligned_tables = add_relative_strength_vs_benchmark(aligned_tables, benchmark_symbol)
    aligned_tables = add_volatility_liquidity_rank_features(aligned_tables)

    output_rows = {s: len(t) for s, t in aligned_tables.items()}

    # Collect columns
    if aligned_tables:
        sample_df = list(aligned_tables.values())[0]
        computed_cols = advanced_feature_columns_from_dataframe(sample_df)
    else:
        computed_cols = []

    result = AdvancedFeatureComputationResult(
        result_id=create_advanced_feature_result_id(),
        created_at_utc=_now(),
        request_id=None,
        symbols=list(aligned_tables.keys()),
        computed_feature_columns=computed_cols,
        computed_family_counts={},
        input_rows_by_symbol=input_rows,
        output_rows_by_symbol=output_rows,
        normalization_results=all_norm_results,
        cross_sectional_alignment=align_result,
        quality=AdvancedFeatureQuality.HIGH,
        output_paths={},
        metadata_only=False,
        dry_run_only=True,
        research_data_only=True,
        computed_values=True,
        produced_trade_signal=False,
        produced_order_decision=False,
        produced_portfolio_weights=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        passed=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    return aligned_tables, result

def write_multi_symbol_advanced_feature_tables(tables: Dict[str, pd.DataFrame], output_dir: Path, overwrite: bool = False) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for sym, df in tables.items():
        out_file = output_dir / f"{sym}_advanced_features.csv"
        if out_file.exists() and not overwrite:
            continue
        df.to_csv(out_file, index=False)
        paths[sym] = str(out_file)
    return paths

def multi_symbol_feature_table_summary(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    return {
        "symbols": list(tables.keys()),
        "table_count": len(tables),
        "columns": list(tables.values())[0].columns.tolist() if tables else []
    }
