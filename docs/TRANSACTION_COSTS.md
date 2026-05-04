# Transaction Cost Models

This document explains the transaction cost models implemented in Phase 26 of the USA Signal Bot.

## Purpose
The transaction cost model estimates broker commissions and regulatory fees applied to simulated backtest fills. Because this engine is entirely local and does not route live or paper orders to any real broker, these costs are **estimates** and do not reflect any guaranteed live market conditions.

## Supported Models

1. **NONE**: Zero fees. Assumes totally free trading.
2. **FLAT_FEE**: Applies a static dollar amount per executed order or fill.
3. **BPS (Basis Points)**: Cost is a percentage of the total notional value of the trade.
   `notional * fee_bps / 10000`
4. **PER_SHARE**: Cost is based on the number of shares traded.
   `quantity * per_share_fee`
5. **COMBINED**: Sums flat fee, bps, and per_share components.

## Configuration Options
- `min_fee`: Minimum dollar value to charge per transaction.
- `max_fee`: Maximum dollar value to charge per transaction.

## Backtesting Output
The model computes an `effective_fee_bps` to illustrate the relative cost of minimum and flat fees against the notional size of the trade. Fees are deducted directly from the portfolio's cash balance when a simulated fill occurs.

## CLI Usage
To see your current cost and slippage settings:
```bash
python -m usa_signal_bot backtest-cost-info
```
