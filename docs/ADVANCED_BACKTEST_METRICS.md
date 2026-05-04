# Advanced Backtest Metrics

The advanced metrics engine provides deeper insights into backtest performance beyond basic returns.

**Important:** These metrics are historical simulations and do not guarantee future performance.

## Key Metrics

- **Total Return / Annualized Return**: The overall growth of the portfolio. Annualized return estimates the yearly growth rate.
- **Max Drawdown**: The largest peak-to-trough drop in portfolio equity.
- **Calmar-like Ratio**: Annualized return divided by the max drawdown percentage.
- **Sharpe-like Ratio**: The mean of equity returns divided by their standard deviation, annualized. Assumes a risk-free rate of 0 for simplicity.
- **Sortino-like Ratio**: Similar to the Sharpe ratio, but only penalizes downside volatility.
- **Win Rate**: The percentage of closed trades that resulted in a positive Net PnL.
- **Profit Factor**: Gross profit divided by gross loss. A value > 1 indicates a profitable strategy.
- **Expectancy**: The expected return per trade based on the average win, average loss, and win rate.

## Breakdowns

The engine also generates performance breakdowns grouped by:
- **Strategy**: Performance metrics for each strategy utilized in the run.
- **Symbol**: Performance metrics for each traded ticker symbol.

## CLI Usage

View advanced metrics for the latest run:

```bash
python -m usa_signal_bot backtest-advanced-metrics --latest
```
