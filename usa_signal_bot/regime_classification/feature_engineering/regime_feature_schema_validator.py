try:
    import pandas as pd
except ImportError:
    pass

def validate_regime_feature_dataframe_schema(df) -> list[str]:
    errors = []
    cols = [str(c).lower() for c in df.columns]
    if "buy_signal" in cols: errors.append("buy_signal not allowed")
    return errors
