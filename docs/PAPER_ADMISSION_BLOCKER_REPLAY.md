# Paper Admission Blocker Replay

## Purpose
The paper admission blocker replay engine provides a local, metadata-only verification that any attempt to admit candidates into a paper environment is strictly blocked.

## Architecture
- Evaluates rules that deny paper trading.
- Replays various attempt types (ENABLE_ACTIVE_PAPER, CREATE_PAPER_ORDER, SEND_BROKER_ORDER).
- Ensures that `blocked=True` and `admission_allowed=False` for all attempts.

## CLI Usage
- `python -m usa_signal_bot blocker-replay-plan --write`
- `python -m usa_signal_bot blocker-replay-run --write`
- `python -m usa_signal_bot blocker-replay-analyze --write`
