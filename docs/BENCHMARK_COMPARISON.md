# Benchmark Comparison

The Benchmark Comparison module allows you to evaluate the equity curve of a strategy backtest against simple passive buy-and-hold returns of common benchmarks (e.g., SPY, QQQ, IWM, CASH).

## Purpose
It provides relative performance context to strategy results.

## Benchmarks
The default set includes:
- **SPY** (SPDR S&P 500 ETF)
- **QQQ** (Invesco QQQ Trust)
- **IWM** (iShares Russell 2000 ETF)
- **CASH** (Cash baseline, constant equity)

## Architecture & Data
Benchmark market data is **loaded directly from the local cache**. The comparison tool will *not* download data from the internet on its own. If cache data is missing, the tool generates warnings and instructs you to download it via data pipelines or `universe` tools.

## Alignment and Metrics
To ensure fair comparison:
- The strategy equity curve and benchmark equity curve are aligned on matching timestamps.
- **Strategy Return** and **Benchmark Return** are compared to compute the **Excess Return**.
- **Relative Drawdown** calculates the difference between Strategy Max Drawdown and Benchmark Max Drawdown.

## "Like" Estimations
We include simple proxy estimations for volatility and risk-adjusted comparisons:
- **Correlation-like**: Simple Pearson correlation of period-to-period curve returns.
- **Beta-like**: Covariance divided by variance of benchmark returns.
- **Tracking-Error-like**: Standard deviation of excess returns (annualized).
- **Information-Ratio-like**: Annualized mean excess return divided by tracking error.

*Note: These are simplified research estimations, not strictly defined institutional financial metrics.*

## CLI Usage

View available benchmark sets:
```bash
python -m usa_signal_bot benchmark-info
```

Check cache readiness for a benchmark set:
```bash
python -m usa_signal_bot benchmark-cache-check --set default --timeframe 1d
```

Compare a specific backtest run against the default benchmark set:
```bash
python -m usa_signal_bot backtest-benchmark-compare --latest --set default --write
```
