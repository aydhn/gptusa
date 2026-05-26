import pandas as pd
def compute_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    sig = macd.ewm(span=signal, adjust=False).mean()
    return macd, sig, macd - sig
def add_macd_features(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    macd, sig, hist = compute_macd(df[price_col])
    df['macd_12_26'] = macd
    df['macd_signal_9'] = sig
    df['macd_hist'] = hist
    return df
def validate_macd_features(df: pd.DataFrame) -> list[str]: return []
def macd_features_summary(df: pd.DataFrame) -> dict: return {}
