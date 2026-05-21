# Observer Safety Guards

Phase 76 implements rigorous safety validations to ensure the Paper Observer subsystem remains non-executing.

## Flagging System
Any output, context, or policy definition that violates the non-executing constraint is flagged with `ObserverSafetyFlag` values, including:
*   `REAL_ORDER_RISK`
*   `PAPER_ORDER_RISK`
*   `BROKER_ORDER_RISK`
*   `PAPER_STATE_MUTATION_RISK`
*   `TELEGRAM_REAL_SEND_RISK`
*   `PRODUCTION_CONFIG_WRITE_RISK`
*   `ACTIVE_PAPER_ENABLE_RISK`
*   `OBSERVER_UNLOCK_RISK`

## Validation Checks
The `runtime_safety_validator.py` and `observer_validation.py` actively scan for:
*   `is_real_order == True`
*   `sends_to_broker == True`
*   `mutates_paper_state == True`
*   Presence of broker-specific fields (`broker_order_id`, `real_fill_id`).
*   Presence of live execution language in notifications ("gerçek emir", "kesin al", "garanti").

## CLI Usage
Execute a safety validation on the current observer runtime logic:
```bash
python -m usa_signal_bot observer-runtime-safety-check --write
```

Run structural and string validation on the latest paper observer review:
```bash
python -m usa_signal_bot paper-observer-validate --latest-review
```
