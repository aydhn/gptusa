# Cost-Adjusted Backtests and Paper Trading

This subsystem adapts gross simulated trades into net results by attaching expected heuristic transaction costs to backtest records and paper trading events.

## Features
*   **Trade Net PnL**: Calculated by subtracting estimated total costs from gross PnL.
*   **Candidate Suppression**: Signals generating excessive estimated transaction costs (e.g. illiquid names with large target notionals) can be suppressed automatically.
*   **Basket Adjustments**: Simulates overall portfolio turnover drag.

## CLI Usage

```bash
python -m usa_signal_bot transaction-cost-review --write
```
