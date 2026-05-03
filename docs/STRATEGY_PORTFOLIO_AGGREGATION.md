# Strategy Portfolio Aggregation

The Strategy Portfolio Aggregation layer is responsible for running multiple strategies simultaneously, evaluating their overlapping confidence (confluence), ranking their output, and finally selecting the best candidates globally.

## Purpose

Instead of assessing one strategy in a vacuum, this layer gathers outputs from several strategies or "rule sets". It groups them into a shared pool, calculating confluence scores for symbols that trigger on multiple fronts, ranking them collectively, and outputting an optimized, diversified watchlist.

## Portfolio Modes

The behavior can be altered via `StrategyPortfolioMode`:
- **`SINGLE_BEST_PER_SYMBOL`**: Eliminates duplicate signals per ticker, keeping only the highest rank.
- **`MULTI_STRATEGY_CONFLUENCE`**: Explicitly requires and heavily weights symbols triggered by multiple strategies simultaneously.
- **`DIVERSIFIED_STRATEGIES`**: Ensures candidate selection enforces diversity across varying rule types.
- **`RESEARCH_POOL`** (Default): Merges all outputs, performing aggregation and ranking to output an indiscriminate pool of top-rated signals.

## The Pipeline Flow

1.  **Strategy Execution**: Runs an array of independent strategies over feature store data.
2.  **Quality Guard & Scoring**: Rejects malformed signals.
3.  **Confluence**: Adjusts confidence depending on multi-strategy alignment.
4.  **Ranking**: Sorts the pooled signals assigning bounded scores.
5.  **Aggregation/Collapse**: Groups identical/overlapping signals on the same timeframe.
6.  **Candidate Selection**: Sifts top entries enforcing limit allocations.

**Disclaimer**: This phase operates strictly as an aggregation and filtering tool. No risk engines, live market checks, paper trading, or live brokerage routing take place here.

## CLI Usage Examples

Run a specific array of strategies across specific tickers:
```bash
python -m usa_signal_bot strategy-portfolio-run --strategies trend_following_rule,momentum_continuation_rule --symbols AAPL,MSFT --timeframes 1d --write
```

Execute an established rule strategy set over feature store data:
```bash
python -m usa_signal_bot rule-strategy-run-ranked --set basic_rules --symbols AAPL,MSFT --timeframes 1d --write
```
