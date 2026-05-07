# Simulated Order Lifecycle

All paper orders created by the system are tracked via a strict state machine to simulate the mechanics of a typical order lifecycle, without communicating with external services.

## Lifecycle States
An order transitions through the following states:
1. `CREATED`: The initial intent is packaged into an order.
2. `VALIDATED`: Checked against internal constraints (cash, limits).
3. `ACCEPTED`: Assumed to be theoretically valid for the market.
4. `QUEUED`: Pushed to the simulated fill engine.
5. `FILLED` / `PARTIALLY_FILLED`: Simulated execution produced matching fills.

## Terminal States
- `FILLED`: Fully executed.
- `REJECTED`: Fails validation (e.g. insufficient cash, short selling blocked).
- `CANCELLED`: Interrupted before fill.
- `EXPIRED`: Time in force elapsed.
- `SKIPPED`: In `dry_run` mode, orders are skipped instead of filled.

## Simulated Fills
Simulated fills use basic rules:
- `fee_bps` and `slippage_bps` are applied artificially to the cache data prices.
- If buying, the effective price is pushed higher by slippage.
- If selling, the effective price is pushed lower by slippage.
- Fees are deducted from cash post-execution.

## CLI Example
```bash
python -m usa_signal_bot paper-run-from-risk --latest-risk --execution-mode local_simulated --write
```
