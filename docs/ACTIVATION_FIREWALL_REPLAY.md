# Activation Firewall Replay

## Purpose
The activation firewall replay checks if the activation processes were successfully blocked.

## Disclaimer
This is metadata-only. No real activation happens here.

## Required Attempt Types
- ENABLE_ACTIVE_PAPER
- ENABLE_CANDIDATE_STRATEGY
- PATCH_PAPER_CONFIG
- COMMIT_PAPER_STATE
- CREATE_PAPER_ORDER
- SEND_BROKER_ORDER
- SEND_TELEGRAM_REAL
- UNLOCK_ARCHIVE
- UNLOCK_FINAL_LOCK

If `allowed_attempt_count > 0`, it blocks the process.

## CLI Examples
- `python -m usa_signal_bot activation-replay-plan --write`
- `python -m usa_signal_bot activation-replay-run --write`
- `python -m usa_signal_bot activation-replay-analyze --write`
