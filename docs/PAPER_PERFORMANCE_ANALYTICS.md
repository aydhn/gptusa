# Paper Performance Analytics

The Paper Performance Analytics module provides a completely local, simulated performance report for virtual paper accounts. This allows users to evaluate their paper runs directly from the terminal without involving real money, external APIs, or dashboards.

## Key Metrics
- **Equity Metrics**: Starting/ending equity, absolute return, total return %, peak/trough, and maximum drawdown.
- **Trade Metrics**: Total open/closed trades, win/loss rate, average win/loss, profit factor, expectancy, best/worst trade, and max win/loss streak.
- **Exposure Metrics**: Average/max gross and net exposure, open position counts, and exposure-to-equity ratio.

## Performance Bucket & Trend
The system classifies overall performance into deterministic buckets (`STRONG`, `ACCEPTABLE`, `WEAK`, `POOR`, `INSUFFICIENT_DATA`) and trend directions (`IMPROVING`, `STABLE`, `DETERIORATING`, `MIXED`).

> **Warning:** This is purely simulated local performance. It does not account for real liquidity, market gaps, or slippage. It is NOT a guarantee of real performance, nor is it investment advice.

## Example CLI Usage
To view paper performance locally:
```bash
python -m usa_signal_bot paper-analytics-info
python -m usa_signal_bot paper-performance-report --latest-paper --write
```
