# Quarantine Safety Guards

The Quarantine system employs strict validation guards to ensure no real operations accidentally trigger.

## Checked Risks
1. **Paper State Mutation Risk**: Blocks `paper_state_mutation_enabled=True`.
2. **Paper Order Risk**: Blocks `paper_order_enabled=True`.
3. **Broker Order Risk**: Blocks `broker_order_enabled=True`.
4. **Telegram Real Send Risk**: Blocks `telegram_real_send_enabled=True`.
5. **Production Config Write Risk**: Blocks `production_config_write_enabled=True`.

## Field and Language Scanners
* **Broker Fields**: Detects and blocks payloads containing `broker_order_id`, `live_order_id`, `execution_venue`.
* **Paper Fields**: Detects and blocks `paper_state_committed`, `paper_order_executed`.
* **Language Scanner**: Rejects reporting text containing "live approved", "sent to broker", "kesin al", "aktif et".
* **Secret Scanner**: Ensures sensitive keys (`api_key`, `secret`) are redacted.

## CLI Examples
```bash
python -m usa_signal_bot quarantine-safety-check --write
python -m usa_signal_bot paper-quarantine-validate --latest-review
```
