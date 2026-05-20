# Sandboxed Paper-Shadow Rehearsal

The Paper-Shadow Rehearsal system allows candidate bundles to be tested in an isolated simulation environment without mutating real paper trading state or sending real orders to any broker.

## Key Concepts
- **Isolated Simulation:** Runs in memory, outputting only to isolated paths.
- **Shadow Order Intents:** Simulated orders that are never dispatched.
- **Shadow Fills:** Simulated execution results (cost, slippage).
- **Shadow Portfolio:** A copy-only or fresh mock portfolio state.

## CLI Usage
```bash
python -m usa_signal_bot paper-shadow-info
python -m usa_signal_bot shadow-session-run --runtime-mode full_paper_shadow --equity 100000
python -m usa_signal_bot paper-shadow-review
```
