# Final Handoff Safety Guards

The system strictly enforces the following non-execution compliance rules:
- `allows_active_paper` MUST be false.
- `allows_broker_execution` MUST be false.
- `allows_paper_state_mutation` MUST be false.
- `allows_config_patch` MUST be false.
- Detection of terms like "sent to broker", "live approved", "kesin al" will fail validation.

CLI Usage:
```
python -m usa_signal_bot final-handoff-safety-check --write
python -m usa_signal_bot final-handoff-validate --latest-review
```
