# Isolated Simulation Session

## ShadowSimulationContext
Defines the strictly isolated environment for the paper-shadow rehearsal.

## Key Properties
- `allow_real_orders`: Always `False`.
- `allow_broker_calls`: Always `False`.
- `allow_paper_state_mutation`: Always `False`.
- `allow_telegram_real_send`: Always `False`.
- `allow_production_config_write`: Always `False`.

## CLI Usage
```bash
python -m usa_signal_bot shadow-context --equity 100000
python -m usa_signal_bot shadow-portfolio-init --equity 100000
```
