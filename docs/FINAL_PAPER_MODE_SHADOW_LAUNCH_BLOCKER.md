# Final Paper Mode Shadow Launch Blocker

## Purpose
The Shadow-Launch Blocker simulates the behavior of dangerous events (such as starting a local paper runtime, sending a broker order) to assert that they would be blocked in a non-execution environment.

## ALL ATTEMPTS DENIED
This component does not open paper mode or shadow launches. It actively blocks attempts.

## Coverage
Rules exist to block attempts like:
- `START_PAPER_MODE`
- `SHADOW_LAUNCH_CANDIDATE`
- `SEND_BROKER_ORDER`
- `COMMIT_PAPER_STATE`

## CLI Usage
```bash
python -m usa_signal_bot shadow-launch-blocker-rules --write
python -m usa_signal_bot shadow-launch-blocker-evaluate --attempt-type start_paper_mode --write
python -m usa_signal_bot shadow-launch-attempt-simulate --write
```
