from typing import Any
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorScoringSpec,
    FactorTableResult,
    FactorScoringResult,
    FactorScoreQuality,
    create_factor_table_id,
    create_factor_scoring_result_id
)
from usa_signal_bot.feature_engine.factor_scoring.factor_scoring_registry import build_factor_scoring_specs
from usa_signal_bot.feature_engine.factor_scoring.individual_factor_scorer import add_individual_factor_scores
from usa_signal_bot.feature_engine.factor_scoring.composite_factor_scorer import add_composite_factor_score
from usa_signal_bot.feature_engine.factor_scoring.factor_normalization import normalize_factor_columns
from usa_signal_bot.feature_engine.factor_scoring.factor_table_schema import build_factor_table_schema
from usa_signal_bot.feature_engine.factor_scoring.cross_sectional_factor_ranks import (
    add_cross_sectional_factor_zscores,
    add_cross_sectional_factor_percentiles,
    add_cross_sectional_factor_ranks
)

def add_all_factor_scores(df: pd.DataFrame, specs: list[FactorScoringSpec] | None = None) -> pd.DataFrame:
    df_out = add_individual_factor_scores(df)
    df_out = add_composite_factor_score(df_out)
    return df_out

def factor_columns_from_dataframe(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if "factor" in c]

def raw_factor_columns_from_dataframe(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if "factor_raw" in c]

def normalized_factor_columns_from_dataframe(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if "zscore" in c]

def percentile_factor_columns_from_dataframe(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if "percentile" in c]

def rank_factor_columns_from_dataframe(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if "rank" in c and "percentile" not in c]

def build_factor_table_result(symbol: str, df: pd.DataFrame, output_path: str | None = None) -> FactorTableResult:
    schema = build_factor_table_schema(df)
    cols = list(df.columns)

    return FactorTableResult(
        table_id=create_factor_table_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        rows=len(df),
        columns=cols,
        factor_columns=factor_columns_from_dataframe(df),
        raw_factor_columns=raw_factor_columns_from_dataframe(df),
        normalized_factor_columns=normalized_factor_columns_from_dataframe(df),
        percentile_factor_columns=percentile_factor_columns_from_dataframe(df),
        rank_factor_columns=rank_factor_columns_from_dataframe(df),
        diagnostics_columns=[],
        null_summary={},
        quality=FactorScoreQuality.ACCEPTABLE,
        schema=schema,
        output_path=output_path,
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

def build_factor_table_for_symbol(symbol: str, df: pd.DataFrame, specs: list[FactorScoringSpec] | None = None) -> tuple[pd.DataFrame, FactorTableResult]:
    if specs is None:
        specs = build_factor_scoring_specs()

    df_out = add_all_factor_scores(df, specs)
    df_out, norm_results = normalize_factor_columns(df_out, specs)
    res = build_factor_table_result(symbol, df_out)
    return df_out, res

def build_factor_tables(paths: dict[str, Path], specs: list[FactorScoringSpec] | None = None) -> tuple[dict[str, pd.DataFrame], FactorScoringResult]:
    from usa_signal_bot.feature_engine.factor_scoring.factor_table_input_loader import load_factor_input_table_csv

    if specs is None:
        specs = build_factor_scoring_specs()

    tables = {}
    norm_res_all = []

    for symbol, p in paths.items():
        df = load_factor_input_table_csv(p)
        df_out = add_all_factor_scores(df, specs)
        df_out, norm_results = normalize_factor_columns(df_out, specs)
        tables[symbol] = df_out
        norm_res_all.extend(norm_results)

    raw_cols = []
    if tables:
        first_df = list(tables.values())[0]
        raw_cols = raw_factor_columns_from_dataframe(first_df)

    # cross sectional
    tables = add_cross_sectional_factor_zscores(tables, raw_cols)
    tables = add_cross_sectional_factor_percentiles(tables, raw_cols)
    tables = add_cross_sectional_factor_ranks(tables, raw_cols)

    all_factor_cols = []
    if tables:
        first_df = list(tables.values())[0]
        all_factor_cols = factor_columns_from_dataframe(first_df)

    result = FactorScoringResult(
        result_id=create_factor_scoring_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        request_id=None,
        symbols=list(tables.keys()),
        factor_names=[s.factor_name for s in specs],
        factor_columns=all_factor_cols,
        raw_factor_columns=raw_cols,
        normalized_factor_columns=[c for c in all_factor_cols if "zscore" in c],
        percentile_factor_columns=[c for c in all_factor_cols if "percentile" in c],
        rank_factor_columns=[c for c in all_factor_cols if "rank" in c and "percentile" not in c],
        normalization_results=norm_res_all,
        diagnostics_profiles=[],
        quality=FactorScoreQuality.ACCEPTABLE,
        output_paths={},
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
    return tables, result

def write_factor_tables(tables: dict[str, pd.DataFrame], output_dir: Path, overwrite: bool = False) -> dict[str, str]:
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for symbol, df in tables.items():
        out_path = output_dir / f"{symbol}_factor_table.csv"
        if out_path.exists() and not overwrite:
            continue
        df.to_csv(out_path, index=False)
        paths[symbol] = str(out_path)
    return paths

def factor_table_builder_summary(tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    return {"status": "ok"}
