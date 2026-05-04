# Buy and Hold Baseline

The Buy and Hold baseline engine generates a simple equity curve simulating holding a specific asset over a period of time.

## Concept
It simulates buying an asset at the *first available open price* and holding it until the *last available close price*.

## Features
- **Fractional Quantities:** By default, allows purchasing fractional shares based on the `starting_cash`.
- **Cash Baseline:** A special baseline mode that produces a flat equity curve representing uninvested cash.
- **Trade Advice Disclaimer:** The buy and hold baseline is meant purely for research context and is not a strategy or investment advice.

## CLI Usage

Generate a buy-and-hold baseline for SPY:
```bash
python -m usa_signal_bot buy-and-hold-baseline --symbol SPY --timeframe 1d --starting-cash 100000
```
