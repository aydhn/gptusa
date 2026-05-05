# Position Sizing Rules

The Position Sizing module computes the theoretical position size for a candidate signal. **Position sizing results are simulated and are not financial advice or live investment directions.**

## Sizing Methods
The engine supports the following methods (`PositionSizingMethod`):

- **FIXED_NOTIONAL**: Allocates a static monetary amount (e.g., $5,000) for the candidate.
- **FIXED_FRACTIONAL**: Computes size as a percentage of the entire portfolio equity (e.g., 5% of $100,000).
- **VOLATILITY_ADJUSTED**: Decreases the target notional dynamically when the asset's observed volatility is high, preventing outsized risk in erratic markets.
- **ATR_RISK**: Determines the number of shares to allocate based on the `average_true_range` (ATR) and a predefined maximum risk tolerance amount per trade (e.g., 1% equity risk with a 2.0x ATR stop loss distance).
- **EQUAL_WEIGHT**: Disperses portfolio equity evenly across a target number of positions.
- **ZERO_SIZE**: Explicitly allocates 0.0 quantity, typically serving as a fallback for missing data or rejection scenarios.

## Caps and Fractions
Every method routes through a central cap enforcer that guarantees the raw notional value respects `max_notional` and `min_notional` limits. The `allow_fractional_quantity` config parameter controls whether the resulting quantity is a float or is floor-rounded to the nearest integer.

## CLI Preview
Test sizing strategies dynamically without executing operations:
`python -m usa_signal_bot position-size-preview --symbol AAPL --price 100 --equity 100000 --cash 50000 --method fixed_notional`
