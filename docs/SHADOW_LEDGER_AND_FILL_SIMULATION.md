# Shadow Ledger and Fill Simulation

To properly analyze a shadow rehearsal, we maintain an independent shadow ledger and perform deterministic fill simulations.

## Shadow Ledger
The shadow ledger captures key events throughout the session without exposing any secret or broker-related fields. Events include:
- `SESSION_STARTED`
- `SIGNAL_PREVIEWED`
- `CANDIDATE_SELECTED`
- `ORDER_INTENT_CREATED`
- `FILL_SIMULATED`
- `PNL_UPDATED`

## Fill Simulation
Fills are purely simulated. They do not represent real executions.
- Slippage and cost are calculated deterministically.
- There are no broker fill IDs.

## Command Line Interface (CLI)
```bash
python -m usa_signal_bot shadow-fill-simulate --write
python -m usa_signal_bot shadow-ledger --write
python -m usa_signal_bot shadow-pnl --equity 100000 --write
```
