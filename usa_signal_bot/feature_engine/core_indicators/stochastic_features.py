import pandas as pd
def compute_stochastic_k(df: pd.DataFrame, window: int = 14) -> pd.Series:
    roll_min = df['low'].rolling(window).min()
    roll_max = df['high'].rolling(window).max()
    return 100 * (df['close'] - roll_min) / (roll_max - roll_min)
def compute_stochastic_d(k_series: pd.Series, smooth: int = 3) -> pd.Series: return k_series.rolling(smooth).mean()
def add_stochastic_features(df: pd.DataFrame) -> pd.DataFrame:
    df['stoch_k_14'] = compute_stochastic_k(df, 14)
    df['stoch_d_3'] = compute_stochastic_d(df['stoch_k_14'], 3)
    return df
def validate_stochastic_features(df: pd.DataFrame) -> list[str]: return []
def stochastic_features_summary(df: pd.DataFrame) -> dict: return {}
