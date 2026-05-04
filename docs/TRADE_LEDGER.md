# Trade Ledger

The Trade Ledger transforms raw backtest fills into a structured list of completed and open trades.

**Important:** The Trade Ledger is a simulated historical record for backtesting analysis. It is not a real brokerage account statement.

## Pairing Logic

The ledger uses a simple FIFO (First-In-First-Out) approach to pair `BUY` fills with `SELL` fills for the same symbol. Currently, the system assumes long-only trades.

## Open and Closed Trades

- **Closed Trades**: A `BUY` fill matched with a subsequent `SELL` fill. PnL and return percentages are fully realized.
- **Open Trades**: A `BUY` fill without a matching `SELL` fill. The position is considered open, and the net PnL currently reflects the entry transaction costs.

## PnL and Costs

- **Gross PnL**: The raw profit or loss of the trade before transaction costs. Note that the fill prices used for Gross PnL *already* include the impact of slippage.
- **Net PnL**: Gross PnL minus transaction fees.
- **Slippage Reporting**: Total slippage cost is tracked separately for reporting, but is not deducted again from Net PnL (as it is already baked into the fill prices).

## CLI Usage

View the trade ledger for the latest run:

```bash
python -m usa_signal_bot backtest-trade-ledger --latest
```
