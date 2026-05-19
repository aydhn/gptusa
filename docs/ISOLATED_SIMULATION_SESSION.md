# Isolated Simulation Session

The isolated simulation session (`ShadowSimulationContext`) forms the foundation for running a shadow rehearsal. It guarantees that the execution environment cannot affect the real application state.

## Characteristics
- **In-Memory Configuration:** Configuration parameters are loaded into memory and any attempt to write them back to production files is blocked (`allow_production_config_write=False`).
- **Isolated Outputs:** Results and artifacts are directed to isolated output paths (e.g., `data/paper_shadow/outputs/isolated`).
- **Strictly No Side Effects:**
  - `allow_broker_calls=False`
  - `allow_real_orders=False`
  - `allow_paper_state_mutation=False`
  - `allow_telegram_real_send=False`

## Command Line Interface (CLI)
```bash
python -m usa_signal_bot shadow-context --equity 100000 --write
python -m usa_signal_bot shadow-portfolio-init --equity 100000 --write
```
