# Adjusted Price Validation

## Purpose
Ensures that the `close` and `adj_close` data within an asset's history makes sense. It highlights when `adj_close` has large discrepancies, which might distort historical backtesting logic.

## Usage
`python -m usa_signal_bot adjusted-price-validate --symbol SPY`
