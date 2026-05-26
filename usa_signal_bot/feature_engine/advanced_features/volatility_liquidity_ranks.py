import pandas as pd
from typing import List, Dict, Any
from usa_signal_bot.feature_engine.advanced_features.cross_sectional_features import add_cross_sectional_percentile_rank, add_cross_sectional_zscore

def add_volatility_rank_features(tables: Dict[str, pd.DataFrame], volatility_col: str = "realized_vol_20") -> Dict[str, pd.DataFrame]:
    """Adds cross-sectional ranks for volatility."""
    tables = add_cross_sectional_percentile_rank(tables, volatility_col, output_column=f"cs_{volatility_col}_rank")
    return tables

def add_liquidity_rank_features(tables: Dict[str, pd.DataFrame], volume_col: str = "volume") -> Dict[str, pd.DataFrame]:
    """Adds cross-sectional ranks for liquidity/volume."""
    # Compute basic volume SMA first if missing
    for sym, df in tables.items():
        if volume_col in df.columns:
            if "volume_sma_20" not in df.columns:
                df["volume_sma_20"] = df[volume_col].rolling(20, min_periods=10).mean()
        tables[sym] = df

    tables = add_cross_sectional_percentile_rank(tables, "volume_sma_20", output_column="cs_liquidity_rank_20")
    tables = add_cross_sectional_zscore(tables, "volume_sma_20", output_column="cs_volume_zscore_rank_20")

    return tables

def add_volatility_liquidity_rank_features(tables: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Runs all volatility and liquidity ranking functions."""
    tables = add_volatility_rank_features(tables)
    tables = add_liquidity_rank_features(tables)
    return tables

def validate_volatility_liquidity_ranks(tables: Dict[str, pd.DataFrame]) -> List[str]:
    errors = []
    for sym, df in tables.items():
        if 'cs_realized_vol_20_rank' not in df.columns:
            errors.append(f'{sym} missing cs_realized_vol_20_rank')
        if 'cs_liquidity_rank_20' not in df.columns:
            errors.append(f'{sym} missing cs_liquidity_rank_20')
    return errors

def volatility_liquidity_ranks_summary(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    if not tables: return {}
    sym = list(tables.keys())[0]
    cols = [c for c in tables[sym].columns if c in ["cs_realized_vol_20_rank", "cs_liquidity_rank_20", "cs_volume_zscore_rank_20"]]
    return {"rank_columns": cols}
