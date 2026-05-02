# Composite Features

In Phase 20, we introduced a robust composite feature orchestration system that unifies our individual feature packs (Trend, Momentum, Volatility, Volume, Price Action, Divergence) into a single, cohesive execution pipeline.

## What is a Composite Feature?
A composite feature is simply a collection of feature groups calculated in a single execution. The orchestration system doesn't generate trading signals—it just calculates all the different technical indicator metrics, organizing the outputs effectively. This approach prevents disjointed runs for different indicator sets and brings everything into a singular data workflow.

## Feature Groups
The system defines several `FeatureGroupType` categories:
- **BASIC**: Simple metrics (e.g., closing return, rolling highs)
- **TREND**: Trend indicators (e.g., SMAs, EMAs, MACD)
- **MOMENTUM**: Momentum oscillators (e.g., RSI, Stochastic, CCI)
- **VOLATILITY**: Volatility metrics (e.g., ATR, Bollinger Bands, Keltner Channels)
- **VOLUME**: Volume indicators (e.g., OBV, VWAP, MFI)
- **PRICE_ACTION**: Price action metrics (e.g., Doji logic, inside bars, market structure)
- **DIVERGENCE**: Price vs. Oscillator divergence detection

These are registered in the `FeatureGroupRegistry` during runtime, meaning you can toggle groups on or off without affecting other parts of the system.

## Composite Feature Sets
We also have several preset configurations (referred to as "Composite Sets") that determine which feature groups are processed together:

- **minimal**: Includes only basic and trend features. Good for lightweight processing or testing.
- **core**: Includes trend, momentum, volatility, and volume features. This represents the primary dataset for standard modeling.
- **technical**: A superset of core that also includes price action features.
- **full**: Includes everything in technical plus divergence features.
- **research**: Currently mirrors the `full` set, but serves as a placeholder for experimental or heavy indicator bundles in future phases.

*Note: These feature bundles serve as the foundational input vectors for strategies, machine learning models, or manual heuristic rules. They DO NOT produce buy/sell signals on their own.*

## CLI Commands
The CLI provides several commands to inspect and execute composite features:

**List Available Feature Groups:**
```bash
python -m usa_signal_bot feature-groups
```

**View Composite Set Configuration:**
```bash
python -m usa_signal_bot composite-feature-set-info --set core
```

**Compute Composite Features from Cache:**
*(Requires OHLCV data to already be present in cache)*
```bash
python -m usa_signal_bot composite-feature-compute-cache --symbols AAPL,MSFT --timeframes 1d --set core --write
```
