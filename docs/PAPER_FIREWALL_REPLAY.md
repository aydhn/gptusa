# Paper Firewall Replay

Firewall replay validates that all dangerous operations attempt blocked.
It operates strictly on metadata and does not execute any actual live code.

## Key Principles
- **No real execution:** Replay is a metadata validation, not a real execution.
- **Dangerous attempt coverage:** Validates coverage for mutation and order events.
- **Not an activation:** Passing the replay does not automatically activate paper trading.

## Commands
```bash
python -m usa_signal_bot firewall-replay-plan --write
python -m usa_signal_bot firewall-replay-run --write
python -m usa_signal_bot firewall-replay-analyze --write
```
