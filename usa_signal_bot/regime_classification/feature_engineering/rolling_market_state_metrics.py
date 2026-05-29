try:
    import pandas as pd
except ImportError:
    pass

def add_rolling_market_state_metrics(df, windows: list[int] | None = None):
    if windows is None: windows = [20, 60, 120]
    for w in windows:
        for c in [x for x in df.columns if "market_" in x or "factor_" in x]:
            if pd.api.types.is_numeric_dtype(df[c]):
                df[f"{c}_rolling_mean_{w}"] = df[c].rolling(w).mean()
    return df
