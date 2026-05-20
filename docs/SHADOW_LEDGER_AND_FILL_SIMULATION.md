# Shadow Ledger and Fill Simulation

## Shadow Ledger
Records all events during a shadow rehearsal without exposing secrets or broker fields.
Event types include `SESSION_STARTED`, `FILL_SIMULATED`, `SESSION_COMPLETED`, and `BLOCKED_OPERATION`.

## Shadow Fill Simulation
Simulates order fills deterministically using default or provided slippage/cost parameters.
**IMPORTANT:** A shadow fill is NOT a real fill.

## Shadow PnL Tracking
Tracks simulated performance. It does not guarantee future performance.

## CLI Usage
```bash
python -m usa_signal_bot shadow-fill-simulate
python -m usa_signal_bot shadow-ledger
python -m usa_signal_bot shadow-pnl --equity 100000
```
