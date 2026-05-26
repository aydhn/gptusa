import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

def compute_relative_strength(series: pd.Series, benchmark_series: pd.Series) -> pd.Series:
    """Computes relative strength (series / benchmark)."""
    return series / benchmark_series.replace(0, np.nan)

def add_relative_strength_vs_benchmark(tables: Dict[str, pd.DataFrame], benchmark_symbol: str = "SPY", columns: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
    """Adds relative strength columns against a benchmark symbol."""
    if columns is None:
        columns = ["ret_1d", "ret_20d", "momentum_60"]

    if benchmark_symbol not in tables:
        return tables  # Can't compute if benchmark missing

    bench_df = tables[benchmark_symbol]

    for sym, df in tables.items():
        if sym == benchmark_symbol:
            continue

        df_out = df.copy()
        for col in columns:
            if col in df_out.columns and col in bench_df.columns:
                rs_col = f"rs_{col}_vs_{benchmark_symbol.lower()}"

                # If these are returns/momentum, relative strength is often just (1+ret_sym) / (1+ret_bench) - 1
                # or sym - bench. Let's do sym - bench for standard momentum
                df_out[rs_col] = df_out[col] - bench_df[col]

        tables[sym] = df_out

    return tables

def validate_relative_strength_features(tables: Dict[str, pd.DataFrame]) -> List[str]:
    errors = []
    for sym, df in tables.items():
        rs_cols = [c for c in df.columns if c.startswith('rs_')]
        if not rs_cols and len(tables) > 1:
            errors.append(f'{sym} has no relative strength features.')
    return errors

def relative_strength_features_summary(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    if not tables:
        return {}
    syms = list(tables.keys())
    if len(syms) < 2:
        return {}

    # Pick a non-benchmark to check columns
    sym = syms[0] if len(syms) > 1 else syms[-1]
    cols = [c for c in tables[sym].columns if c.startswith("rs_")]
    return {"rs_columns": cols}
