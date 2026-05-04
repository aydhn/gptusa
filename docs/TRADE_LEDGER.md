# Trade Ledger

The Trade Ledger module, introduced in Phase 26, is responsible for matching raw transaction fills into discrete round-trip trades.

## Overview
A `TradeLedger` groups individual `BacktestFill` events (e.g. 10 shares bought, 10 shares sold) into discrete `BacktestTrade` records.

### FIFO Pairing
Since this project defaults to long-only simulated trades in Phase 26, the ledger pairs `SELL` fills against the oldest available `BUY` fills (First-In, First-Out).

### Key Concepts
- **Open Trades**: Fills that have been bought but not yet sold by the end of the backtest.
- **Closed Trades**: Fully matched buy and sell fills.
- **Gross PnL**: The profit or loss generated purely from price differences (`Exit Price - Entry Price` * `Quantity`).
- **Net PnL**: The `Gross PnL` minus `total_fees` computed by the transaction cost model. (Slippage is handled independently by adjusting the `fill_price` directly).

## Important Disclaimer
The `TradeLedger` relies purely on historical data simulation. **It is not a real account statement, and the generated backtest trades do not guarantee equivalent future performance.**

## CLI Usage
To view the trade ledger summary from the most recent run:
```bash
python -m usa_signal_bot backtest-trade-ledger --latest
```
