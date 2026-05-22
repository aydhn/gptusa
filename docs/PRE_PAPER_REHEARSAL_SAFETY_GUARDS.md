# Pre-Paper Rehearsal Safety Guards

This system enforces multiple safety guards during pre-paper rehearsals to explicitly block dangerous or unintended executions.

## Enforced Protections
- **No active paper enable:** Automatically blocks attempts to enable paper trading.
- **No paper state mutation:** Prohibits modification of the paper baseline state.
- **No paper order:** Flags any generation of paper orders.
- **No broker order:** Prevents broker order creation and execution.
- **No Telegram real send:** Blocks actual network calls to Telegram.
- **No production config patch:** Prevents patches to the active configuration.

## Validation and Assertions
If the firewall is disabled or activation is allowed, the system blocks the rehearsal.

## CLI Usage

Assert zero mutations occurred:
```bash
python -m usa_signal_bot zero-mutation-assert --write
```

Validate pre-paper payloads:
```bash
python -m usa_signal_bot pre-paper-validate --latest-review
```
