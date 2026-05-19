# Sandboxed Paper-Shadow Rehearsal

The Paper-Shadow Rehearsal system takes the candidate bundle from the release sandbox (Phase 69) and runs it through an isolated simulation session. The primary goal is to preview how the candidate would behave in a production/paper runtime without actually modifying any real state or interacting with external APIs.

## Concepts

*   **Isolated Simulation Context:** A safe environment where configuration is held in memory and outputs are strictly isolated.
*   **Shadow Order Intent:** Represents a simulated intent to trade. It is definitively NOT a broker order (`is_real_order=False`, `broker_destination=None`).
*   **Shadow Fill:** Represents a simulated execution of a shadow intent. It calculates hypothetical slippage and costs based on deterministic formulas, avoiding any real execution (`is_real_fill=False`).
*   **Safety Guards:** Ensuring that the shadow rehearsal strictly blocks any attempt to make real orders, mutate the actual paper portfolio state, send real Telegram messages, or write to production configuration.

## Command Line Interface (CLI)
Here are some example commands:
```bash
python -m usa_signal_bot paper-shadow-info
python -m usa_signal_bot shadow-session-run --runtime-mode full_paper_shadow --equity 100000 --write
python -m usa_signal_bot paper-shadow-review --write
```
