# Multi-Timeframe Market Data

The USA Signal Bot utilizes a multi-timeframe approach for market data to ensure robust signal generation and context awareness.

## Necessity

Single timeframe analysis is often insufficient for robust trading. A multi-timeframe approach allows algorithms to:
1. Identify the primary trend.
2. Confirm signals on a different timeframe.
3. Optimize entries/exits on an intraday timeframe.

## Timeframe Roles

- **PRIMARY**: The main timeframe for generating signals (default: `1d`).
- **CONFIRMATION**: Used to confirm the primary signal (default: `1h`).
- **INTRADAY**: Used for precise entries/exits or short-term context (default: `15m`).

## Default Timeframes

The default multi-timeframe configuration is:
- `1d` (Primary)
- `1h` (Confirmation)
- `15m` (Intraday)

## Constraints (yfinance)

When using `yfinance` as the provider, note that intraday data is limited (e.g., 60 days for 15m/1h). The system expects fewer bars for intraday data when calculating readiness to avoid false failures.

## Cache Design

The cache is segmented by symbol and timeframe. This allows independent refresh schedules, e.g., refreshing 15m data every 30 minutes while refreshing 1d data only once a day.

## CLI Usage

```bash
# Build a refresh plan across multiple timeframes
python -m usa_signal_bot data-mtf-plan --symbols AAPL,MSFT --timeframes 1d,1h,15m

# Execute the download/refresh pipeline
python -m usa_signal_bot data-mtf-download --symbols AAPL,MSFT --timeframes 1d,1h,15m --limit 2

# Execute for the entire active watchlist universe
python -m usa_signal_bot data-mtf-universe --timeframes 1d,1h --limit 20
```
