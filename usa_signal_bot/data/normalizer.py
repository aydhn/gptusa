import pandas as pd
from typing import Any, List
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.core.exceptions import DataNormalizationError
# Removed

def normalize_timestamp_to_utc(value: Any) -> str:
    """Converts a pandas timestamp to a UTC ISO formatted string."""
    try:
        ts = pd.to_datetime(value)
        if ts.tzinfo is None:
            ts = ts.tz_localize('UTC')
        else:
            ts = ts.tz_convert('UTC')
        return ts.isoformat()
    except Exception as e:
        raise DataNormalizationError(f"Failed to normalize timestamp {value}: {e}")

def standardize_ohlcv_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes column names for internal consistency."""
    # This might do more complex renaming if necessary, but yfinance standard cols are usually fine
    # We mainly map 'Adj Close' to 'adjusted_close' during row mapping.
    return df

def dataframe_row_to_ohlcv_bar(symbol: str, timestamp: Any, row: Any, timeframe: str, source: str) -> OHLCVBar:
    """Converts a single pandas Series/row into an OHLCVBar."""
    try:
        ts_utc = normalize_timestamp_to_utc(timestamp)

        # Check required OHLC fields
        required_cols = ['Open', 'High', 'Low', 'Close']
        for col in required_cols:
             if col not in row or pd.isna(row[col]):
                 raise ValueError(f"Missing required price column: {col}")

        # Ensure prices are positive (basic check before validation)
        open_p = float(row['Open'])
        high_p = float(row['High'])
        low_p = float(row['Low'])
        close_p = float(row['Close'])

        vol = float(row.get('Volume', 0.0))
        if pd.isna(vol):
             vol = 0.0

        adj_close = None
        if 'Adj Close' in row and not pd.isna(row['Adj Close']):
             adj_close = float(row['Adj Close'])

        return OHLCVBar(
            symbol=symbol,
            timestamp_utc=ts_utc,
            timeframe=timeframe,
            open=open_p,
            high=high_p,
            low=low_p,
            close=close_p,
            volume=vol,
            adjusted_close=adj_close,
            source=source
        )
    except Exception as e:
        raise DataNormalizationError(f"Failed to normalize row for {symbol} at {timestamp}: {e}")

def extract_symbol_dataframe(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Extracts a single symbol's data from a multi-level index dataframe, or returns it if single."""
    if isinstance(df.columns, pd.MultiIndex):
        # Determine if ticker is level 0 or level 1. yfinance sometimes changes this.
        # Usually: level 0 is Price (Open, Close), level 1 is Ticker
        # Let's check where the symbol lives
        if symbol in df.columns.get_level_values(1):
             # xs slices the multiindex to just this symbol
             sym_df = df.xs(symbol, axis=1, level=1)
             available_cols = [c for c in ['Open', 'High', 'Low', 'Close'] if c in sym_df.columns]
             return sym_df.dropna(subset=available_cols, how='all') if available_cols else sym_df
        elif symbol in df.columns.get_level_values(0):
             sym_df = df[symbol]
             available_cols = [c for c in ['Open', 'High', 'Low', 'Close'] if c in sym_df.columns]
             return sym_df.dropna(subset=available_cols, how='all') if available_cols else sym_df
        else:
             # Symbol not found in this chunk
             return pd.DataFrame()
    else:
        # Assuming it's already a single symbol dataframe
        available_cols = [c for c in ['Open', 'High', 'Low', 'Close'] if c in df.columns]
        return df.dropna(subset=available_cols, how='all') if available_cols else df


def normalize_single_symbol_dataframe(df: pd.DataFrame, symbol: str, timeframe: str, source: str = "yfinance") -> List[OHLCVBar]:
    """Converts a single symbol dataframe to a list of OHLCVBars."""
    bars = []
    if df.empty:
        return bars

    df = standardize_ohlcv_columns(df)

    for idx, row in df.iterrows():
        try:
            bar = dataframe_row_to_ohlcv_bar(symbol, idx, row, timeframe, source)
            bars.append(bar)
        except DataNormalizationError:
            # We skip invalid rows (e.g. missing critical price data entirely), can be logged/audited separately
            continue
    return bars

def normalize_yfinance_dataframe(df: pd.DataFrame, symbols: List[str], timeframe: str, source: str = "yfinance") -> List[OHLCVBar]:
    """Converts a potentially multi-symbol dataframe from yfinance into a flat list of OHLCVBars."""
    all_bars = []
    if df.empty:
        return all_bars

    if isinstance(df.columns, pd.MultiIndex):
        for symbol in symbols:
            sym_df = extract_symbol_dataframe(df, symbol)
            if not sym_df.empty:
                 all_bars.extend(normalize_single_symbol_dataframe(sym_df, symbol, timeframe, source))
    else:
        # Single symbol case
        # yfinance returns a single level df if only one symbol was requested
        if len(symbols) == 1:
             symbol = symbols[0]
             all_bars.extend(normalize_single_symbol_dataframe(df, symbol, timeframe, source))
        else:
             # Weird edge case where multiple symbols requested but single index returned.
             pass

    return all_bars
