# Shadow Safety Guards

Ensures that the paper-shadow rehearsal remains strictly isolated.

## Checked Risks
- `REAL_ORDER_RISK`: Blocks any attempt to create a real order.
- `PAPER_STATE_MUTATION_RISK`: Blocks any attempt to mutate existing paper portfolios.
- `BROKER_FIELD_RISK`: Blocks use of actual broker identifiers.
- `TELEGRAM_REAL_SEND_RISK`: Blocks real notifications.
- `PRODUCTION_CONFIG_WRITE_RISK`: Blocks mutating real config.

## CLI Usage
```bash
python -m usa_signal_bot shadow-safety-check
python -m usa_signal_bot paper-shadow-validate
```
