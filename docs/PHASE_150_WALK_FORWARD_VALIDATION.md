# Phase 150: Walk Forward Validation

Phase 150 is the offline walk-forward validation and temporal stability audit phase.
It explicitly prohibits live/paper trading, broker integration, deployment, stress tests, and Monte Carlo.
Phase 151 will handle stress testing and Monte Carlo robustness.

CLI examples:
- `python -m usa_signal_bot walk-forward-info`
- `python -m usa_signal_bot build-walk-forward-window-policy --write`
