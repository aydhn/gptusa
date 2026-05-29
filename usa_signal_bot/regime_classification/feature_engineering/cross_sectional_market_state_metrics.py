try:
    import pandas as pd
except ImportError:
    pass

def add_cross_sectional_market_state_metrics(tables: dict):
    for s, df in tables.items():
        if "cross_sectional_dispersion_context" not in df.columns:
            df["cross_sectional_dispersion_context"] = 0.0
    return tables
