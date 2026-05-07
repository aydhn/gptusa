# Local Paper Trading Foundation (Phase 37)

The Local Paper Trading subsystem provides a safe, deterministic, locally simulated paper trading environment for research.

## Purpose
This subsystem exists to:
1. Translate abstract strategy outputs (Risk Decisions, Allocations, Candidates) into tangible `PaperOrderIntent` objects.
2. Manage the lifecycle of these simulated orders (`PaperOrder`).
3. Create artificial execution (`PaperFill`) based on strictly local historical data.
4. Record performance in a virtual cash/position ledger.

## CRITICAL: Not a Broker Interface
**This subsystem DOES NOT connect to any broker.**
- There are no live orders.
- There are no demo orders.
- It does not interact with Alpaca, IBKR, Robinhood, or any other broker API.
- All price resolution is strictly done by reading the local data cache (`LocalPriceResolver`).
- Execution modes available: `validate_only`, `dry_run`, `local_simulated`.

## Execution Modes
- **validate_only**: Validates orders but skips execution.
- **dry_run**: Queues orders but does not produce any fills.
- **local_simulated**: Reads the local cache OHLCV bar to generate an artificial fill with estimated slippage and fees.

## Limitations
- Paper results are not a guarantee of real-world trading performance.
- Simulated slippage and fees are static estimations.
- Real-world liquidity, partial fills, latency, and spread impact are ignored.

## CLI Usage
You can test the components from the CLI:
```bash
python -m usa_signal_bot paper-info
python -m usa_signal_bot paper-order-preview --symbol AAPL --side buy --quantity 1
python -m usa_signal_bot paper-run-from-portfolio --latest-portfolio --execution-mode dry_run
```
