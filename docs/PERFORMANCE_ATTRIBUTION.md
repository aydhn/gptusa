# Performance Attribution

The Performance Attribution module decomposes the overall Net PnL of a backtest run into specific dimensions to identify what worked and what didn't.

## Purpose
To drill down into the trade ledger and summarize performance grouped by key characteristics.

## Supported Dimensions
- **STRATEGY**: PnL grouped by the strategy that generated the signal.
- **SYMBOL**: PnL grouped by individual ticker symbols.
- **TIMEFRAME**: PnL grouped by the signal timeframe (e.g., `1d`, `1h`).
- **ACTION**: PnL grouped by the trade direction (LONG/SHORT).
- **MONTH / YEAR**: PnL grouped by trade exit or entry time to see temporal performance.
- **HOLDING_PERIOD**: PnL grouped by holding duration buckets (0-1, 2-5, 6-20, 21+ bars).

## Contribution Percentage
For each row in a dimension, the `contribution_pct` represents the proportion of that specific group's Net PnL relative to the absolute total Net PnL of the backtest.

*Note: This is a simplified attribution estimation based on closed and partially closed trades. It is not a formal fund performance attribution report.*

## CLI Usage

Generate an attribution report for the latest run:
```bash
python -m usa_signal_bot backtest-attribution --latest --dimensions strategy,symbol,timeframe,month --write
```
