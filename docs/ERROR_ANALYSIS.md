# Error Analysis

This module is responsible for analyzing error events, finding losing trades, false positive signals, cost-degraded events, and drawdown contributors. It provides a foundational layer for understanding system performance but acts strictly as a local heuristic analytics system.

CLI commands:
python -m usa_signal_bot diagnostics-info
python -m usa_signal_bot loss-analysis --dimension strategy
python -m usa_signal_bot false-signal-analysis --min-score 70
