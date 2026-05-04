# Advanced Backtest Metrics

This document outlines the advanced performance and risk metrics added to the backtest engine in Phase 26.

## Purpose
While Phase 25 introduced basic PnL and trade counting, Phase 26 introduces sophisticated analytics to break down strategy performance, understand drawdown profiles, and generate risk-adjusted return proxies.

## Available Metrics

### Trade Analytics
- **Win Rate**: Percentage of trades that were profitable (net PnL > 0).
- **Profit Factor**: Gross Profit divided by the absolute value of Gross Loss.
- **Payoff Ratio**: Average Winning Trade divided by Average Losing Trade.
- **Expectancy**: Expected dollar value return per trade.

### Drawdown Analytics
- **Max Drawdown**: The deepest absolute loss from a previous high water mark.
- **Drawdown Periods**: Tracking the start, trough, and recovery of each dip in equity.

### Equity & Risk Proxies
- **Annualized Return**: Total return scaled to an annual equivalent.
- **Calmar-like Ratio**: Annualized return divided by Max Drawdown percentage.
- **Sharpe-like Ratio**: The average equity return divided by its standard deviation, annualized.
- **Sortino-like Ratio**: Similar to Sharpe, but only penalizes downside volatility.

*Note: The "like" suffix denotes that these are local heuristic implementations, calculated without robust risk-free-rate integrations.*

## Trade Breakdowns
Metrics can be broken down to evaluate performance based on:
- **Strategy Breakdown**: Which specific rule-set/strategy contributed to the returns.
- **Symbol Breakdown**: Which stocks/tickers were most profitable.

## CLI Usage
To view advanced metrics for your most recent backtest:
```bash
python -m usa_signal_bot backtest-advanced-metrics --latest
```

*Reminder: Past performance simulation in this local tool does not guarantee future live market results.*
