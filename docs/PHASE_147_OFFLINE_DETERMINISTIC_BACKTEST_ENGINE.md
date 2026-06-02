# Phase 147: Offline Deterministic Realistic Backtest Engine

Phase 147 handles offline, deterministic, single-strategy backtests.
It strictly prevents real broker integration, paper state mutation, Telegram real send, deployment, and live inference.
It also explicitly excludes multi-strategy/portfolio-optimization and benchmark comparison in this phase (delegated to Phase 148).

Run `python -m usa_signal_bot backtest-run-info` for more information.
